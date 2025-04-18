import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from github_service import GithubService
from models import CodeChange

class TestGithubService(unittest.TestCase):
    
    def setUp(self):
        self.github_service = GithubService("dummy_token")
    
    def test_parse_github_url_repo(self):
        """Test parsing a GitHub repository URL"""
        url = "https://github.com/username/repo"
        result = self.github_service.parse_github_url(url)
        
        self.assertEqual(result["owner"], "username")
        self.assertEqual(result["repo"], "repo")
        self.assertFalse(result["is_pr"])
    
    def test_parse_github_url_pr(self):
        """Test parsing a GitHub PR URL"""
        url = "https://github.com/username/repo/pull/123"
        result = self.github_service.parse_github_url(url)
        
        self.assertEqual(result["owner"], "username")
        self.assertEqual(result["repo"], "repo")
        self.assertEqual(result["pr_number"], 123)
        self.assertTrue(result["is_pr"])
    
    def test_parse_github_url_invalid(self):
        """Test parsing an invalid GitHub URL"""
        url = "https://not-github.com/username/repo"
        
        with self.assertRaises(ValueError):
            self.github_service.parse_github_url(url)
    
    @patch('github_service.Github')
    def test_get_pr_changes(self, mock_github):
        """Test fetching PR changes"""
        # Set up mocks
        mock_repo = MagicMock()
        mock_pr = MagicMock()
        mock_file = MagicMock()
        
        # Configure mock behavior
        mock_github.return_value.get_repo.return_value = mock_repo
        mock_repo.get_pull.return_value = mock_pr
        mock_pr.get_files.return_value = [mock_file]
        mock_file.filename = "test.py"
        mock_file.patch = "test diff"
        mock_file.status = "modified"
        
        # Mock _get_file_content and _is_reviewable_file
        self.github_service._get_file_content = MagicMock(return_value="file content")
        self.github_service._is_reviewable_file = MagicMock(return_value=True)
        
        # Call the method
        changes = self.github_service.get_pr_changes("username", "repo", 123)
        
        # Assertions
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0].file_path, "test.py")
        self.assertEqual(changes[0].content, "file content")
        self.assertEqual(changes[0].diff, "test diff")
        self.assertFalse(changes[0].is_new)
    
    def test_is_reviewable_file(self):
        """Test file filtering for review"""
        # Files that should be included
        self.assertTrue(self.github_service._is_reviewable_file("src/main.py"))
        self.assertTrue(self.github_service._is_reviewable_file("app/components/Button.js"))
        
        # Files that should be excluded
        self.assertFalse(self.github_service._is_reviewable_file("images/logo.png"))
        self.assertFalse(self.github_service._is_reviewable_file("node_modules/package/index.js"))
        self.assertFalse(self.github_service._is_reviewable_file("dist/bundle.min.js"))


if __name__ == '__main__':
    unittest.main()
