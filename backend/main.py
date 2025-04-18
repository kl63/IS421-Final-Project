import logging
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import os
import traceback
from typing import List, Optional
from dotenv import load_dotenv

from github_service import GithubService
from llm_service import LLMService
from models import (
    ReviewRequest, 
    ReviewResponse, 
    Issue, 
    IssueLabel, 
    TestSuggestion,
    ReviewSettings
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Code Review Assistant",
    description="AI-powered code review assistant for GitHub repositories and PRs",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
github_service = GithubService(os.getenv("GITHUB_TOKEN"))
llm_service = LLMService()

@app.get("/")
async def root():
    return {"message": "Code Review Assistant API is running"}

@app.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest, background_tasks: BackgroundTasks):
    """
    Analyze a GitHub repository or PR and return code review suggestions
    """
    try:
        logger.info(f"Received review request for URL: {request.url}")
        
        # Extract repo and PR info from the URL
        repo_info = github_service.parse_github_url(request.url)
        logger.info(f"Parsed GitHub URL: {repo_info}")
        
        # Fetch the code changes
        logger.info("Fetching code changes...")
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
                request.file_paths
            )
        
        logger.info(f"Fetched {len(code_changes)} files for analysis")
        
        # Analyze the code with LLM
        logger.info("Starting code analysis with LLM...")
        analysis = llm_service.analyze_code(
            code_changes, 
            review_settings=request.settings
        )
        
        # Optionally apply labels to GitHub PR
        if request.settings.apply_labels and repo_info["is_pr"]:
            logger.info("Applying labels to PR...")
            background_tasks.add_task(
                github_service.apply_labels,
                repo_info["owner"],
                repo_info["repo"],
                repo_info["pr_number"],
                analysis.issues
            )
        
        logger.info("Review completed successfully")
        return analysis
        
    except Exception as e:
        logger.error(f"Error processing review request: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/export-review")
async def export_review(review: ReviewResponse):
    """
    Export the review to Markdown format
    """
    markdown = llm_service.generate_markdown_report(review)
    return {"markdown": markdown}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
