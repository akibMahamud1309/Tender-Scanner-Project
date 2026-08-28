# 15 --- ERROR HISTORY

Record important errors with date, agent, module, file/function,
environment, versions, error, root cause, fix, tests, and status.

## Error record

```text
Error ID: ERR-001
Date: 2026-08-28 17:05
Agent: Claude (chat session)
System version: 0.1.0
File: .env
Function: N/A (environment setup)
Environment: Windows, VS Code
Error: .env file was accidentally created inside "Project Workflow and Development History - 14 Modules/" subfolder instead of the project root, causing load_dotenv() to return None for DATABASE_URL.
Root cause: File created via right-click in the wrong Explorer subfolder.
Fix: Moved .env and .env.example to the actual project root, next to venv/ and openlink.py. Verified load_dotenv() then correctly returned the connection string.
Tests: Manual verification via `python -c "...load_dotenv()...print(os.getenv('DATABASE_URL'))"`
Status: Resolved
```