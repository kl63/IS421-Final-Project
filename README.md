# IS421 Final Project - Code Review Assistant

An AI-powered code review assistant that analyzes GitHub repositories and pull requests to provide helpful suggestions, identify issues, and generate summaries.

## Features

- Analyze code from GitHub repositories or pull requests
- Provide AI-powered code improvement suggestions
- Auto-label issues (security, style, refactor, test coverage)
- Generate test case suggestions
- Create high-level summaries for non-technical stakeholders

## Tech Stack

- **Backend:** FastAPI with GitHub API integration
- **AI:** Integration with LLMs via MCP
- **Frontend:** Next.js with React
- **Optional:** Webhook integration for PR triggers

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- GitHub API credentials

### Installation

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Configuration

Create a `.env` file in the backend directory with the following:

```
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_api_key  # If using OpenAI directly
```

### Running the Application

Use the start script to run both frontend and backend:
```bash
./start.sh
```

Or run them separately:

1. Start the backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

## Usage

1. Navigate to the web interface
2. Enter a GitHub repository URL or pull request URL
3. Review the AI-generated suggestions and summaries
4. Optionally export reviews or apply labels

## License

MIT
