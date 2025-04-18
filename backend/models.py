from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, Dict, Union
from enum import Enum

class ReviewTone(str, Enum):
    STRICT = "strict"
    MENTOR = "mentor"
    NEUTRAL = "neutral"

class IssueLabel(str, Enum):
    SECURITY = "security"
    STYLE = "style"
    REFACTOR = "refactor"
    TEST_COVERAGE = "test_coverage"
    PERFORMANCE = "performance"
    DOCUMENTATION = "documentation"
    BUG = "bug"

class ReviewSettings(BaseModel):
    tone: ReviewTone = ReviewTone.NEUTRAL
    apply_labels: bool = False
    include_test_suggestions: bool = True
    include_summary: bool = True
    max_issues: int = 10

class Issue(BaseModel):
    title: str
    description: str
    file_path: str
    line_numbers: List[int] = []
    labels: List[IssueLabel] = []
    suggestion: Optional[str] = None
    code_example: Optional[str] = None
    severity: Optional[str] = None

class TestSuggestion(BaseModel):
    file_path: str
    test_description: str
    test_case_example: Optional[str] = None

class ReviewRequest(BaseModel):
    url: HttpUrl = Field(..., description="GitHub repository or PR URL")
    file_paths: Optional[List[str]] = Field(None, description="Specific file paths to review (repo only)")
    settings: ReviewSettings = Field(default_factory=ReviewSettings)

class CodeChange(BaseModel):
    file_path: str
    content: str
    diff: Optional[str] = None
    is_new: bool = False

class ReviewResponse(BaseModel):
    issues: List[Issue] = []
    test_suggestions: List[TestSuggestion] = []
    summary: Optional[str] = None
    suggested_labels: List[IssueLabel] = []
    total_files_analyzed: int
    analysis_time_seconds: float
