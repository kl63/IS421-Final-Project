import json
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv

from github_service import GithubService
from llm_service import LLMService

# Load environment variables
load_dotenv()

# Initialize the MCP server
mcp_app = FastAPI(
    title="Code Review Assistant MCP Server",
    description="MCP server for code review and analysis",
    version="1.0.0",
)

# Add CORS middleware
mcp_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GithubService(os.getenv("GITHUB_TOKEN"))
llm_service = LLMService()

# MCP Request models
class MCPMessage(BaseModel):
    role: str
    content: str

class MCPRequest(BaseModel):
    messages: List[MCPMessage]
    model: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False

class CodeReviewInput(BaseModel):
    url: str
    file_paths: Optional[List[str]] = None
    review_tone: Optional[str] = "neutral"
    include_test_suggestions: Optional[bool] = True
    include_summary: Optional[bool] = True
    max_issues: Optional[int] = 10

class MCPResponse(BaseModel):
    id: str = "mcp-code-review-response"
    model: str
    object: str = "chat.completion"
    created: int
    choices: List[Dict[str, Any]]

@mcp_app.post("/v1/chat/completions")
async def mcp_code_review(request: MCPRequest):
    """
    MCP endpoint for code review services
    """
    import time
    
    # Get the last user message
    user_messages = [m for m in request.messages if m.role == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No user message found")
    
    user_message = user_messages[-1].content
    
    try:
        # Attempt to parse the user's request as a code review request
        input_data = _parse_code_review_request(user_message)
        
        if input_data:
            # Extract repo and PR info from the URL
            repo_info = github_service.parse_github_url(input_data.url)
            
            # Create review settings
            from models import ReviewSettings, ReviewTone
            settings = ReviewSettings(
                tone=ReviewTone(input_data.review_tone),
                include_test_suggestions=input_data.include_test_suggestions,
                include_summary=input_data.include_summary,
                max_issues=input_data.max_issues
            )
            
            # Fetch the code changes
            if repo_info["is_pr"]:
                code_changes = github_service.get_pr_changes(
                    repo_info["owner"], 
                    repo_info["repo"], 
                    repo_info["pr_number"]
                )
            else:
                code_changes = github_service.get_repo_files(
                    repo_info["owner"], 
                    repo_info["repo"],
                    input_data.file_paths
                )
            
            # Analyze the code with LLM
            analysis = llm_service.analyze_code(
                code_changes, 
                review_settings=settings
            )
            
            # Generate a markdown report
            markdown_report = llm_service.generate_markdown_report(analysis)
            
            # Create response content
            response_content = f"""
# Code Review Results

{markdown_report}

## Analysis Summary
- Total files analyzed: {analysis.total_files_analyzed}
- Issues found: {len(analysis.issues)}
- Test suggestions: {len(analysis.test_suggestions)}
- Analysis completed in {analysis.analysis_time_seconds:.2f} seconds
            """
            
            # Create MCP response
            response = {
                "id": "mcp-code-review-" + str(int(time.time())),
                "model": request.model,
                "object": "chat.completion",
                "created": int(time.time()),
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response_content
                        },
                        "finish_reason": "stop"
                    }
                ]
            }
            
            return response
        
        # If not a code review request, return a help message
        return {
            "id": "mcp-code-review-" + str(int(time.time())),
            "model": request.model,
            "object": "chat.completion",
            "created": int(time.time()),
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": """
# Code Review Assistant MCP

This is a Code Review Assistant MCP server that can analyze GitHub repositories or pull requests and provide AI-powered code review suggestions.

## How to use:

1. Provide a GitHub repository or pull request URL
2. Optionally specify file paths to review
3. Configure review settings like tone, test suggestions, etc.

Example request:
```
Please review this GitHub repository: https://github.com/username/repo
```

For more specific reviews:
```
Review this PR with strict tone and focus on security issues: https://github.com/username/repo/pull/123
```
                        """
                    },
                    "finish_reason": "stop"
                }
            ]
        }
        
    except Exception as e:
        # Return error message
        return {
            "id": "mcp-code-review-error-" + str(int(time.time())),
            "model": request.model,
            "object": "chat.completion",
            "created": int(time.time()),
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"Error processing code review request: {str(e)}"
                    },
                    "finish_reason": "stop"
                }
            ]
        }

def _parse_code_review_request(message: str) -> Optional[CodeReviewInput]:
    """
    Parse a user message to extract code review parameters
    """
    import re
    
    # Check for GitHub URL patterns
    url_pattern = r"https://github\.com/[\w-]+/[\w-]+(?:/pull/\d+)?"
    url_match = re.search(url_pattern, message)
    
    if not url_match:
        return None
    
    github_url = url_match.group(0)
    
    # Create default review input
    review_input = CodeReviewInput(url=github_url)
    
    # Check for file paths
    file_paths_pattern = r"file(?:s|path|paths):\s*\[(.*?)\]"
    file_paths_match = re.search(file_paths_pattern, message, re.IGNORECASE | re.DOTALL)
    
    if file_paths_match:
        # Extract file paths, handle both comma and space separated lists
        paths_str = file_paths_match.group(1)
        file_paths = [p.strip().strip('"\'') for p in re.split(r'[,\s]+', paths_str) if p.strip()]
        review_input.file_paths = file_paths
    
    # Check for tone
    tone_pattern = r"tone:\s*(strict|mentor|neutral)"
    tone_match = re.search(tone_pattern, message, re.IGNORECASE)
    
    if tone_match:
        review_input.review_tone = tone_match.group(1).lower()
    
    # Check for max issues
    max_issues_pattern = r"max(?:\s+|-)?issues:\s*(\d+)"
    max_issues_match = re.search(max_issues_pattern, message, re.IGNORECASE)
    
    if max_issues_match:
        review_input.max_issues = int(max_issues_match.group(1))
    
    # Check for boolean flags
    if re.search(r"include\s+test\s+suggestions:\s*(?:false|no)", message, re.IGNORECASE):
        review_input.include_test_suggestions = False
    
    if re.search(r"include\s+summary:\s*(?:false|no)", message, re.IGNORECASE):
        review_input.include_summary = False
    
    return review_input

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("mcp_server:mcp_app", host="0.0.0.0", port=8080, reload=True)
