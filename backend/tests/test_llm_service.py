import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_service import LLMService
from models import ReviewSettings, ReviewTone, CodeChange, ReviewResponse, Issue, IssueLabel, TestSuggestion

class TestLLMService(unittest.TestCase):
    
    def setUp(self):
        self.llm_service = LLMService()
        self.llm_service.client = MagicMock()
    
    def test_prepare_code_content(self):
        """Test preparing code content for LLM analysis"""
        # Create sample code changes
        code_changes = [
            CodeChange(
                file_path="test.py",
                content="def test():\n    return True",
                diff="@@ -0,0 +1,2 @@\n+def test():\n+    return True",
                is_new=True
            ),
            CodeChange(
                file_path="main.py",
                content="print('Hello')",
                is_new=False
            )
        ]
        
        # Prepare content
        result = self.llm_service._prepare_code_content(code_changes)
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertTrue("test.py" in result)
        self.assertTrue("main.py" in result)
        self.assertEqual(result["test.py"]["content"], "def test():\n    return True")
        self.assertEqual(result["test.py"]["diff"], "@@ -0,0 +1,2 @@\n+def test():\n+    return True")
        self.assertTrue(result["test.py"]["is_new"])
        self.assertEqual(result["main.py"]["content"], "print('Hello')")
        self.assertFalse(result["main.py"]["is_new"])
    
    def test_create_analysis_prompt(self):
        """Test creating the analysis prompt with different settings"""
        code_content = {
            "test.py": {
                "content": "def test():\n    return True",
                "is_new": True
            }
        }
        
        # Test with default settings
        settings = ReviewSettings()
        prompt = self.llm_service._create_analysis_prompt(code_content, settings)
        
        # Basic assertions
        self.assertIn("You are an expert code reviewer", prompt)
        self.assertIn("neutral", prompt.lower())
        self.assertIn("test.py", prompt)
        
        # Test with strict tone
        settings.tone = ReviewTone.STRICT
        prompt = self.llm_service._create_analysis_prompt(code_content, settings)
        self.assertIn("Be thorough and critical in your review", prompt)
        
        # Test with mentor tone
        settings.tone = ReviewTone.MENTOR
        prompt = self.llm_service._create_analysis_prompt(code_content, settings)
        self.assertIn("Be constructive and educational", prompt)
    
    @patch('llm_service.LLMService._call_llm')
    def test_analyze_code(self, mock_call_llm):
        """Test analyzing code and generating review response"""
        # Mock LLM response
        mock_call_llm.return_value = """{
            "issues": [
                {
                    "title": "Unused import",
                    "file_path": "test.py",
                    "line_numbers": [1],
                    "description": "Import is not used in the code",
                    "suggestion": "Remove the unused import",
                    "code_example": "# Remove this line\\nimport os",
                    "labels": ["style"]
                }
            ],
            "test_suggestions": [
                {
                    "file_path": "test.py",
                    "test_description": "Test the main function",
                    "test_case_example": "def test_main():\\n    assert main() == True"
                }
            ],
            "summary": "The code has minor style issues",
            "suggested_labels": ["style"]
        }"""
        
        # Create sample code changes
        code_changes = [
            CodeChange(
                file_path="test.py",
                content="import os\n\ndef main():\n    return True",
                is_new=False
            )
        ]
        
        # Analyze code
        result = self.llm_service.analyze_code(code_changes, ReviewSettings())
        
        # Assertions
        self.assertIsInstance(result, ReviewResponse)
        self.assertEqual(len(result.issues), 1)
        self.assertEqual(result.issues[0].title, "Unused import")
        self.assertEqual(result.issues[0].file_path, "test.py")
        self.assertEqual(len(result.test_suggestions), 1)
        self.assertEqual(result.test_suggestions[0].file_path, "test.py")
        self.assertEqual(result.summary, "The code has minor style issues")
        
    def test_generate_markdown_report(self):
        """Test generating markdown report from review response"""
        # Create a sample review response
        review = ReviewResponse(
            issues=[
                Issue(
                    title="Security vulnerability",
                    description="SQL injection risk",
                    file_path="database.py",
                    line_numbers=[45, 46],
                    labels=[IssueLabel.SECURITY],
                    suggestion="Use parameterized queries",
                    code_example="cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
                )
            ],
            test_suggestions=[
                TestSuggestion(
                    file_path="auth.py",
                    test_description="Test authentication flow",
                    test_case_example="def test_auth():\n    assert authenticate('user', 'pass') == True"
                )
            ],
            summary="The code has security issues that need to be addressed",
            suggested_labels=[IssueLabel.SECURITY],
            total_files_analyzed=2,
            analysis_time_seconds=1.5
        )
        
        # Generate markdown
        markdown = self.llm_service.generate_markdown_report(review)
        
        # Assertions
        self.assertIn("# Code Review Report", markdown)
        self.assertIn("## Summary", markdown)
        self.assertIn("The code has security issues", markdown)
        self.assertIn("## Issues Found", markdown)
        self.assertIn("Security vulnerability", markdown)
        self.assertIn("database.py", markdown)
        self.assertIn("## Test Suggestions", markdown)
        self.assertIn("auth.py", markdown)


if __name__ == '__main__':
    unittest.main()
