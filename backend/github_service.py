import re
import base64
import logging
from typing import Dict, List, Optional, Any
from github import Github, GithubException
from models import IssueLabel, Issue, CodeChange

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GithubService:
    def __init__(self, github_token: str):
        """Initialize GitHub service with authentication token"""
        logger.info("Initializing GitHub service")
        self.github = Github(github_token)
    
    def parse_github_url(self, url: str) -> Dict[str, Any]:
        """
        Parse a GitHub URL to extract owner, repo, and PR number if applicable
        
        Examples:
        - https://github.com/owner/repo
        - https://github.com/owner/repo/pull/123
        """
        logger.info(f"Parsing GitHub URL: {url}")
        # PR URL pattern
        pr_pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        pr_match = re.match(pr_pattern, str(url))
        
        if pr_match:
            result = {
                "owner": pr_match.group(1),
                "repo": pr_match.group(2),
                "pr_number": int(pr_match.group(3)),
                "is_pr": True
            }
            logger.info(f"Parsed PR URL: {result}")
            return result
        
        # Repo URL pattern
        repo_pattern = r"https://github\.com/([^/]+)/([^/]+)"
        repo_match = re.match(repo_pattern, str(url))
        
        if repo_match:
            result = {
                "owner": repo_match.group(1),
                "repo": repo_match.group(2),
                "is_pr": False
            }
            logger.info(f"Parsed repo URL: {result}")
            return result
        
        logger.error(f"Invalid GitHub URL: {url}")
        raise ValueError(f"Invalid GitHub URL: {url}")
    
    def get_pr_changes(self, owner: str, repo_name: str, pr_number: int) -> List[CodeChange]:
        """Get all file changes from a specific pull request"""
        try:
            logger.info(f"Getting PR changes for {owner}/{repo_name} PR #{pr_number}")
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            pull_request = repo.get_pull(pr_number)
            
            changes = []
            for file in pull_request.get_files():
                logger.info(f"Processing file: {file.filename}")
                if self._is_reviewable_file(file.filename):
                    try:
                        content = self._get_file_content(repo, file.filename, pull_request.head.sha)
                        changes.append(CodeChange(
                            file_path=file.filename,
                            content=content,
                            diff=file.patch if file.patch else "",
                            is_new=file.status == "added"
                        ))
                    except Exception as e:
                        logger.error(f"Error processing file {file.filename}: {e}")
                else:
                    logger.info(f"Skipping non-reviewable file: {file.filename}")
            
            logger.info(f"Found {len(changes)} reviewable files in PR")
            return changes
            
        except Exception as e:
            logger.error(f"Error getting PR changes: {str(e)}")
            raise
    
    def get_repo_files(self, owner: str, repo_name: str, file_paths: Optional[List[str]] = None) -> List[CodeChange]:
        """Get files from a repository, optionally filtering by file paths"""
        try:
            logger.info(f"Getting files from repo: {owner}/{repo_name}")
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            
            changes = []
            
            if file_paths:
                logger.info(f"Using specific file paths: {file_paths}")
                for path in file_paths:
                    try:
                        if self._is_reviewable_file(path):
                            content = self._get_file_content(repo, path)
                            changes.append(CodeChange(
                                file_path=path,
                                content=content,
                                diff="",
                                is_new=False
                            ))
                    except Exception as e:
                        logger.error(f"Error processing file {path}: {e}")
            else:
                logger.info("Getting all files from repository")
                contents = repo.get_contents("")
                scanned_files = 0
                max_files = 50  # Limit to prevent API abuse
                
                while contents and scanned_files < max_files:
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        try:
                            contents.extend(repo.get_contents(file_content.path))
                        except Exception as e:
                            logger.error(f"Error accessing directory {file_content.path}: {e}")
                    else:
                        scanned_files += 1
                        if self._is_reviewable_file(file_content.path):
                            try:
                                content = self._get_file_content_safe(repo, file_content.path)
                                changes.append(CodeChange(
                                    file_path=file_content.path,
                                    content=content,
                                    diff="",
                                    is_new=False
                                ))
                            except Exception as e:
                                logger.error(f"Error processing file {file_content.path}: {e}")
                
                logger.info(f"Scanned {scanned_files} files, found {len(changes)} reviewable files")
            
            return changes
            
        except Exception as e:
            logger.error(f"Error getting repo files: {str(e)}")
            raise
    
    def apply_labels(self, owner: str, repo_name: str, pr_number: int, issues: List[Issue]):
        """Apply labels to a PR based on detected issues"""
        try:
            logger.info(f"Applying labels to PR #{pr_number}")
            repo = self.github.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)
            
            # Extract unique labels from issues
            labels = set()
            for issue in issues:
                for label in issue.labels:
                    labels.add(label)
            
            # Create labels if they don't exist
            for label in labels:
                try:
                    label_name = label.name.lower()
                    try:
                        repo.get_label(label_name)
                    except:
                        self._create_label(repo, label)
                    
                    # Add label to PR
                    pr.add_to_labels(label_name)
                    logger.info(f"Added label {label_name} to PR")
                except Exception as e:
                    logger.error(f"Error adding label {label}: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying labels: {str(e)}")
    
    def _create_label(self, repo, label_name: IssueLabel):
        """Create a new label in the repository if it doesn't exist"""
        logger.info(f"Creating label: {label_name}")
        try:
            colors = {
                IssueLabel.SECURITY: "d93f0b",      # red
                IssueLabel.STYLE: "c5def5",         # light blue
                IssueLabel.REFACTOR: "cc68dd",      # purple
                IssueLabel.TEST_COVERAGE: "fbca04", # yellow
                IssueLabel.PERFORMANCE: "ffb8c6",   # pink
                IssueLabel.DOCUMENTATION: "0e8a16", # green
                IssueLabel.BUG: "d93f0b",           # orange
                IssueLabel.ERROR: "ff0000",         # bright red
            }
            
            color = colors.get(label_name, "cccccc")  # default gray
            repo.create_label(label_name, color, f"AI-detected {label_name} issue")
            logger.info(f"Created label {label_name} with color {color}")
        except Exception as e:
            logger.error(f"Error creating label {label_name}: {str(e)}")
    
    def _get_file_content_safe(self, repo, file_path: str, ref: str = None) -> str:
        """Safe wrapper around _get_file_content with additional error handling"""
        try:
            return self._get_file_content(repo, file_path, ref)
        except Exception as e:
            logger.error(f"Error in _get_file_content_safe for {file_path}: {str(e)}")
            return f"[Error reading file: {file_path}]"
    
    def _get_file_content(self, repo, file_path: str, ref: str = None) -> str:
        """Get the content of a file from a repository"""
        try:
            logger.info(f"Getting content for file: {file_path}")
            content = repo.get_contents(file_path, ref=ref)
            
            # Skip binary files and very large files
            if content.size > 500000:  # Skip files larger than 500KB
                logger.warning(f"Skipping large file: {file_path} ({content.size} bytes)")
                return f"[File too large to analyze: {file_path} ({content.size} bytes)]"
            
            # First decode from base64
            try:
                decoded_content = base64.b64decode(content.content)
                
                # Try to detect if this is a text file by attempting to decode as utf-8
                try:
                    return decoded_content.decode('utf-8')
                except UnicodeDecodeError:
                    logger.warning(f"Unable to decode file as UTF-8: {file_path}")
                    # Try with error handling
                    try:
                        return decoded_content.decode('utf-8', errors='replace')
                    except:
                        # If all else fails, return a placeholder
                        logger.warning(f"File appears to be binary: {file_path}")
                        return f"[Binary file not displayed: {file_path}]"
            except Exception as e:
                logger.error(f"Error decoding base64 content: {str(e)}")
                return f"[Error decoding content: {str(e)}]"
                
        except Exception as e:
            logger.error(f"Error retrieving file content: {str(e)}")
            return f"[Error retrieving file: {str(e)}]"
    
    def _is_reviewable_file(self, file_path: str) -> bool:
        """Check if a file should be included in code review"""
        logger.debug(f"Checking if file is reviewable: {file_path}")
        
        # Skip binary files, images, etc.
        skip_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', 
                           '.zip', '.tar', '.gz', '.pyc', '.min.js', '.min.css',
                           '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4', '.mov',
                           '.avi', '.exe', '.dll', '.so', '.dylib', '.class', '.jar']
        
        # Skip certain directories
        skip_directories = ['node_modules/', 'venv/', 'dist/', 'build/', '.git/',
                           '__pycache__/', '.idea/', '.vscode/']
        
        # Check file extension
        file_ext = '.' + file_path.split('.')[-1].lower() if '.' in file_path else ''
        if file_ext in skip_extensions:
            logger.debug(f"Skipping file with extension {file_ext}: {file_path}")
            return False
        
        # Check directories
        for directory in skip_directories:
            if directory in file_path:
                logger.debug(f"Skipping file in directory {directory}: {file_path}")
                return False
        
        # Assume it's reviewable if it passed all checks
        return True
