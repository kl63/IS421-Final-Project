# Code Review Assistant MCP Integration

This document describes how to integrate the Code Review Assistant MCP server with other systems.

## Overview

The Code Review Assistant MCP server implements the Model Control Protocol (MCP) interface, allowing it to be used as a language model provider with enhanced capabilities for code review.

## API Endpoints

### MCP Chat Completions API

```
POST /v1/chat/completions
```

This endpoint is compatible with the OpenAI Chat Completions API format, making it easy to integrate with existing systems.

#### Request Format

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a code review assistant."
    },
    {
      "role": "user",
      "content": "Please review this GitHub repository: https://github.com/username/repo"
    }
  ],
  "model": "code-review-assistant",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### Response Format

```json
{
  "id": "mcp-code-review-1234567890",
  "model": "code-review-assistant",
  "object": "chat.completion",
  "created": 1617834283,
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "# Code Review Results\n\n## Summary\n\nThis repository has several issues including potential security vulnerabilities and code style inconsistencies...",
      },
      "finish_reason": "stop"
    }
  ]
}
```

## Usage Examples

### Basic Repository Review

To review an entire GitHub repository:

```
Please review this GitHub repository: https://github.com/username/repo
```

### Pull Request Review

To review a specific pull request:

```
Review this PR: https://github.com/username/repo/pull/123
```

### Advanced Options

You can specify various review options:

```
Review https://github.com/username/repo with the following settings:
- tone: strict
- max-issues: 20
- include test suggestions: yes
- include summary: yes
- files: ["src/main.js", "lib/utils.js"]
```

## Integration with LLM Frameworks

### LangChain Integration

```python
from langchain.chat_models import ChatOpenAI

# Configure the MCP endpoint
code_review_llm = ChatOpenAI(
    base_url="http://localhost:8080/v1",
    model="code-review-assistant",
    api_key="dummy-key" # Not required but needs to be set
)

# Use the MCP server for code review
response = code_review_llm.invoke([
    {"role": "user", "content": "Review this repo: https://github.com/username/repo"}
])
```

### Direct API Usage

```python
import requests

response = requests.post(
    "http://localhost:8080/v1/chat/completions",
    json={
        "messages": [
            {"role": "user", "content": "Review this PR: https://github.com/username/repo/pull/123"}
        ],
        "model": "code-review-assistant"
    }
)

print(response.json())
```

## Deployment

The MCP server can be deployed as a standalone service or alongside the main application. See the Docker documentation for deployment options.

## Limitations

- The MCP server requires a valid GitHub API token with appropriate permissions
- Large repositories may take longer to process
- Private repositories require appropriate authentication
