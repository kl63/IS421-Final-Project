# 🚀 Windsurf Request: Build a Code Review Assistant MCP Server

## 🧠 Idea
Create a Code Review Assistant that takes a GitHub repository or pull request (PR) URL as input and returns AI-powered code review suggestions.

## 🧩 Input
- GitHub repo URL or PR URL

## 🎯 Output
- Suggested code improvements
- Auto-labeled issues (e.g., `security`, `style`, `refactor`, `test coverage`)
- Test case suggestions
- High-level change summary for PMs or non-technical stakeholders

## 🔧 Features
- Use the GitHub API to pull code diffs or full files from PRs
- Analyze code with an LLM and return:
  - Specific issues or anti-patterns
  - Suggestions for improvement (with code examples)
  - Suggested test cases if missing
  - A TL;DR summary for PMs
- Auto-apply labels using GitHub API (optional)
- Display results in a clean UI or JSON output

## 🛠️ Tech Stack
- **Backend:** FastAPI or Node.js with GitHub API integration
- **LLM:** OpenAI, Claude, or local model via MCP
- **Frontend:** Minimal web interface using Next.js or React
- **Optional:** Webhook integration to trigger reviews when new PRs are opened

## 🧪 Example Flow
1. User pastes a GitHub PR URL.
2. Server fetches the diff or changed files.
3. LLM analyzes the code and generates review suggestions.
4. Server returns:
   - Labeled issues (e.g., "Security: Use of unsafe eval()")
   - Suggested improvements (e.g., "Consider using map instead of for-loop")
   - Summary: "This PR adds a new API endpoint and updates validation logic"

## 💡 Bonus Ideas
- Add a “Review Again” button after edits
- Export reviews to Markdown for documentation
- Allow different tone settings: strict reviewer vs mentor mode

---

Use this spec to build the full MCP server. Focus on automation, helpful insights, and a great dev experience.
