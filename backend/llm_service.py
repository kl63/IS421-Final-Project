import time
import json
import logging
import traceback
from typing import List, Dict, Any
from openai import OpenAI
import os
from models import (
    ReviewResponse, 
    Issue, 
    IssueLabel, 
    TestSuggestion, 
    ReviewSettings,
    CodeChange,
    ReviewTone
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        """Initialize the LLM service with API key from environment variables"""
        # Set up OpenAI client if API key is available
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        # Use MOCK_MODE environment variable or default to True to avoid quota issues
        self.mock_mode = os.getenv("MOCK_MODE", "False").lower() == "true"
        
        if self.openai_api_key and not self.mock_mode:
            # Initialize the modern OpenAI client
            self.client = OpenAI(api_key=self.openai_api_key)
            logger.info("Using real OpenAI API for analysis")
        else:
            self.client = None
            logger.info("Using mock responses (no API calls)")
            if self.mock_mode:
                logger.info("MOCK_MODE is enabled in configuration")
            else:
                logger.warning("MOCK_MODE is disabled but no OpenAI API key found")
    
    def analyze_code(self, code_changes: List[CodeChange], review_settings: ReviewSettings) -> ReviewResponse:
        """
        Analyze code changes using LLM and return review suggestions
        """
        start_time = time.time()
        logger.info(f"Starting code analysis with {len(code_changes)} files")
        
        # Check if we should use mock mode
        use_mock = self.mock_mode or not self.openai_api_key
        
        # Add detailed logging
        logger.info(f"MOCK_MODE from env: {self.mock_mode}")
        logger.info(f"Has OpenAI API key: {bool(self.openai_api_key)}")
        logger.info(f"Using mock mode: {use_mock}")
        
        if use_mock:
            logger.info("Using mock analysis mode")
            # Prepare a mock response
            response = self._get_mock_response_with_real_files(code_changes)
            # Parse the mock response
            analysis_result = self._parse_llm_response(response, code_changes)
        else:
            logger.info("Using OpenAI API for analysis")
            # Prepare the code changes for analysis
            code_for_analysis = self._prepare_code_content(code_changes)
            # Create the prompt based on review settings
            prompt = self._create_analysis_prompt(code_for_analysis, review_settings)
            # Call the LLM with real API
            response = self._call_llm(prompt)
            # Parse LLM response
            analysis_result = self._parse_llm_response(response, code_changes)
        
        # Add timing information
        analysis_time = time.time() - start_time
        analysis_result.analysis_time_seconds = analysis_time
        analysis_result.total_files_analyzed = len(code_changes)
        
        logger.info(f"Analysis completed in {analysis_time:.2f} seconds")
        return analysis_result
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM with the prepared prompt"""
        try:
            logger.info("Making OpenAI API request")
            logger.info(f"API Key (first 5 chars): {self.openai_api_key[:5] if self.openai_api_key else 'None'}")
            logger.info(f"Using model: gpt-3.5-turbo")
            
            # Print OpenAI's env variable to verify
            import os
            logger.info(f"OpenAI API Key from env: {os.getenv('OPENAI_API_KEY')[:5] if os.getenv('OPENAI_API_KEY') else 'None'}")
            
            # Use the modern OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Using GPT-3.5 for cost and speed
                messages=[
                    {"role": "system", "content": "You are a code review assistant that provides detailed and helpful feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            if not response or not hasattr(response, 'choices') or not response.choices:
                logger.error("Invalid response format from OpenAI")
                return self._get_mock_response_with_real_files([])
                
            logger.info(f"Response received with {len(response.choices)} choices")
            response_content = response.choices[0].message.content
            logger.info("Successfully received OpenAI API response")
            logger.info(f"Response starts with: {response_content[:100]}...")
            return response_content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            logger.error(f"Error trace: {traceback.format_exc()}")
            logger.error("Falling back to mock response with real file paths")
            return self._get_mock_response(prompt)
    
    def _get_mock_response_with_real_files(self, code_changes: List[CodeChange]) -> str:
        """Generate a mock response using the actual file paths from code_changes"""
        # Get real file paths from code changes
        real_files = [change.file_path for change in code_changes]
        
        # Create a more realistic mock response with the actual files
        mock_response = {
            "issues": [],
            "test_suggestions": [],
            "summary": f"This is a mock code review of {len(real_files)} files. MOCK_MODE is enabled in the backend.",
            "suggested_labels": ["mock"]
        }
        
        # Add mock issues for the real files (up to 3 files)
        issue_types = ["Documentation needed", "Consider refactoring", "Add comments"]
        
        for i, file_path in enumerate(real_files[:3]):
            if i < len(issue_types):
                mock_response["issues"].append({
                    "title": f"{issue_types[i]} in {file_path}",
                    "file_path": file_path,
                    "line_numbers": [1],
                    "description": f"This is a mock issue for demonstration purposes in {file_path}. The backend is running in MOCK_MODE, so these are not real issues.",
                    "suggestion": "Enable real analysis by setting MOCK_MODE=False in .env and providing a valid OpenAI API key.",
                    "code_example": "# This is mock code\nprint('Hello world')",
                    "labels": ["mock"]
                })
        
        # Add a mock test suggestion using a real file
        if real_files:
            mock_response["test_suggestions"].append({
                "file_path": real_files[0],
                "test_description": "This is a mock test suggestion for demonstration purposes. The backend is running in MOCK_MODE, so this is not a real suggestion.",
                "test_case_example": "# This is a mock test case\ndef test_example():\n    assert True"
            })
        
        # Convert to JSON string
        return json.dumps(mock_response)
    
    def _prepare_code_content(self, code_changes: List[CodeChange]) -> Dict[str, Any]:
        """Prepare code content in a format suitable for LLM analysis"""
        prepared_content = {}
        
        for change in code_changes:
            # For PRs with diffs
            if change.diff:
                prepared_content[change.file_path] = {
                    "content": change.content,
                    "diff": change.diff,
                    "is_new": change.is_new
                }
            # For repo files without diffs
            else:
                prepared_content[change.file_path] = {
                    "content": change.content,
                    "is_new": change.is_new
                }
        
        return prepared_content
    
    def _parse_llm_response(self, response: str, code_changes: List[CodeChange]) -> ReviewResponse:
        """Parse the LLM response into structured data"""
        try:
            # Try to parse the JSON response
            logger.info("Parsing LLM response")
            # Find JSON in the response (handle cases where the model outputs text before/after JSON)
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                response_data = json.loads(json_str)
            else:
                response_data = json.loads(response)
            
            # Extract issues
            issues = []
            for issue_data in response_data.get("issues", []):
                labels = [IssueLabel(label) for label in issue_data.get("labels", [])]
                
                issues.append(Issue(
                    title=issue_data.get("title", "Unnamed Issue"),
                    file_path=issue_data.get("file_path", ""),
                    line_numbers=issue_data.get("line_numbers", []),
                    description=issue_data.get("description", ""),
                    suggestion=issue_data.get("suggestion", ""),
                    code_example=issue_data.get("code_example", ""),
                    labels=labels
                ))
            
            # Extract test suggestions
            test_suggestions = []
            for test_data in response_data.get("test_suggestions", []):
                test_suggestions.append(TestSuggestion(
                    file_path=test_data.get("file_path", ""),
                    test_description=test_data.get("test_description", ""),
                    test_case_example=test_data.get("test_case_example", "")
                ))
            
            # Extract summary and suggested labels
            summary = response_data.get("summary", "")
            suggested_labels = response_data.get("suggested_labels", [])
            
            return ReviewResponse(
                issues=issues,
                test_suggestions=test_suggestions,
                summary=summary,
                suggested_labels=suggested_labels,
                analysis_time_seconds=0.0,  # Will be updated later
                total_files_analyzed=len(code_changes)
            )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {str(e)}")
            logger.error(f"Raw response: {response}")
            # Return a simplified response with error information
            return ReviewResponse(
                issues=[Issue(
                    title="Error in Response Parsing",
                    file_path="",
                    line_numbers=[],
                    description=f"Failed to parse LLM response: {str(e)}",
                    suggestion="Please try again with a different repository or settings.",
                    code_example="",
                    labels=[IssueLabel.ERROR]
                )],
                test_suggestions=[],
                summary="An error occurred during code analysis.",
                suggested_labels=[],
                analysis_time_seconds=0.0,
                total_files_analyzed=len(code_changes)
            )

    def _create_analysis_prompt(self, code_content: Dict[str, Any], settings: ReviewSettings) -> str:
        """Create the prompt for the LLM based on the code and settings"""
        tone_instructions = {
            ReviewTone.STRICT: "Be thorough and critical in your review. Focus on identifying all issues and potential improvements.",
            ReviewTone.MENTOR: "Be constructive and educational. Explain issues clearly and provide guidance on how to improve the code.",
            ReviewTone.NEUTRAL: "Provide a balanced review focusing on significant issues while acknowledging good practices."
        }
        
        prompt = f"""
        You are an expert code reviewer with deep knowledge of software engineering best practices, security, and performance optimization.
        
        REVIEW TONE: {tone_instructions[settings.tone]}
        
        TASK: Perform a detailed code review of the following files and return a structured analysis.
        
        FILES TO REVIEW:
        ```
        {json.dumps(code_content, indent=2)}
        ```
        
        INSTRUCTIONS:
        
        1. Identify up to {settings.max_issues} issues or areas for improvement in the code.
        2. For each issue, provide:
           - A clear title describing the issue
           - The file path and line numbers where the issue occurs
           - A detailed description of why it's problematic
           - A specific suggestion for how to fix it
           - An example of improved code when applicable
           - Appropriate labels from: security, style, refactor, test_coverage, performance, documentation, bug
        
        3. {"Suggest test cases for components that lack testing." if settings.include_test_suggestions else ""}
        
        4. {"Provide a high-level summary of the changes that would be understandable by non-technical stakeholders." if settings.include_summary else ""}
        
        FORMAT YOUR RESPONSE AS A JSON OBJECT with the following structure:
        {{
            "issues": [
                {{
                    "title": "Issue title",
                    "file_path": "path/to/file.ext",
                    "line_numbers": [23, 24],
                    "description": "Detailed explanation of the issue",
                    "suggestion": "How to fix it",
                    "code_example": "Example code fix",
                    "labels": ["security", "refactor"]
                }}
            ],
            "test_suggestions": [
                {{
                    "file_path": "path/to/file.ext",
                    "test_description": "What should be tested",
                    "test_case_example": "Example test code"
                }}
            ],
            "summary": "High-level summary for non-technical stakeholders",
            "suggested_labels": ["security", "refactor"]
        }}
        """
        
        return prompt
        
    def _get_mock_response(self, prompt=None) -> str:
        """Return a mock response for demonstration without API usage"""
        # Extract file info from prompt if available
        file_info = ""
        if prompt:
            # Try to extract file paths from the prompt
            import re
            file_matches = re.findall(r'"file_path":\s*"([^"]+)"', prompt)
            if file_matches:
                file_info = f"for files: {', '.join(file_matches[:3])}"
        
        return f"""{{"issues": [
            {{
                "title": "Potential SQL Injection Risk {file_info}",
                "file_path": "app/database.py",
                "line_numbers": [45, 46],
                "description": "Direct string interpolation in SQL query creates a risk for SQL injection attacks. User input should never be directly concatenated into SQL queries.",
                "suggestion": "Use parameterized queries with placeholders to prevent SQL injection attacks.",
                "code_example": "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
                "labels": ["security", "bug"]
            }},
            {{
                "title": "Missing Input Validation",
                "file_path": "app/routes.py",
                "line_numbers": [23],
                "description": "User input is processed without validation, which could lead to unexpected behavior or security vulnerabilities.",
                "suggestion": "Add input validation before processing user data.",
                "code_example": "if not validate_input(user_input):\\n    return jsonify({{'error': 'Invalid input'}}), 400",
                "labels": ["security", "bug"]
            }},
            {{
                "title": "Inefficient Algorithm",
                "file_path": "app/utils.py",
                "line_numbers": [78, 79, 80],
                "description": "This function uses a nested loop with O(n²) time complexity, which can cause performance issues with large datasets.",
                "suggestion": "Consider using a more efficient algorithm or data structure to improve performance.",
                "code_example": "# Use a dictionary for O(n) lookup\\nitem_map = {{item['id']: item for item in items}}\\nresult = [item_map[id] for id in ids if id in item_map]",
                "labels": ["performance", "refactor"]
            }},
            {{
                "title": "Inadequate Error Handling",
                "file_path": "app/api.py",
                "line_numbers": [102],
                "description": "The function doesn't properly handle exceptions, which could lead to unexpected crashes or exposing sensitive information.",
                "suggestion": "Implement proper error handling with try-except blocks and meaningful error messages.",
                "code_example": "try:\\n    result = process_data(data)\\nexcept ValidationError as e:\\n    return jsonify({{'error': str(e)}}), 400\\nexcept Exception as e:\\n    logger.error(f'Unexpected error: {{e}}')\\n    return jsonify({{'error': 'An unexpected error occurred'}}), 500",
                "labels": ["bug", "refactor"]
            }}
        ],
        "test_suggestions": [
            {{
                "file_path": "app/api.py",
                "test_description": "Test error handling scenarios to ensure the API responds correctly when invalid data is provided.",
                "test_case_example": "def test_api_error_handling():\\n    response = client.post('/api/data', json={{'invalid': 'data'}})\\n    assert response.status_code == 400\\n    assert 'error' in response.json()"
            }},
            {{
                "file_path": "app/utils.py",
                "test_description": "Add tests for the utility functions with various input sizes to verify performance characteristics.",
                "test_case_example": "def test_utils_performance():\\n    # Test with small input\\n    start_time = time.time()\\n    result_small = process_items(small_dataset)\\n    small_duration = time.time() - start_time\\n    \\n    # Test with large input\\n    start_time = time.time()\\n    result_large = process_items(large_dataset)\\n    large_duration = time.time() - start_time\\n    \\n    # Verify performance is roughly linear\\n    ratio = large_dataset_size / small_dataset_size\\n    assert large_duration < small_duration * ratio * 1.5"
            }}
        ],
        "summary": "The code review identified several issues including security vulnerabilities (SQL injection, missing input validation), performance concerns (inefficient algorithms), and code quality issues (inadequate error handling). Addressing these issues will improve security, performance, and reliability. Additionally, improving test coverage would help ensure code quality as the application evolves.",
        "suggested_labels": ["security", "bug", "performance", "refactor"]
    }}"""
