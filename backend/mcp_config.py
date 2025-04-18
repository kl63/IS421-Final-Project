"""
MCP Server Configuration for Code Review Assistant

This module contains configuration settings for the MCP server integration.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MCP Server Configuration
MCP_SERVER_CONFIG = {
    "name": "code-review-assistant",
    "version": "1.0.0",
    "description": "AI-powered code review assistant for GitHub repositories and PRs",
    "port": int(os.getenv("MCP_PORT", 8080)),
    "host": os.getenv("MCP_HOST", "0.0.0.0"),
    
    # Model Configuration
    "model_info": {
        "id": "code-review-assistant",
        "capabilities": {
            "chat": True,
            "function_calling": False,
            "vision": False,
            "embeddings": False
        },
        "parameters": {
            "temperature": {
                "type": "float",
                "min": 0.0,
                "max": 1.0,
                "default": 0.7,
                "description": "Controls randomness of the output"
            },
            "max_tokens": {
                "type": "integer",
                "min": 1,
                "max": 4000,
                "default": 1000,
                "description": "Maximum number of tokens to generate"
            }
        }
    },
    
    # Authentication
    "auth": {
        "enabled": os.getenv("MCP_AUTH_ENABLED", "false").lower() == "true",
        "api_key": os.getenv("MCP_API_KEY", "")
    },
    
    # GitHub Integration
    "github": {
        "token": os.getenv("GITHUB_TOKEN", ""),
        "max_files_per_repo": int(os.getenv("MAX_FILES_PER_REPO", 50)),
        "max_files_per_pr": int(os.getenv("MAX_FILES_PER_PR", 30))
    },
    
    # Logging
    "logging": {
        "level": os.getenv("LOG_LEVEL", "INFO"),
        "file": os.getenv("LOG_FILE", ""),
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    }
}
