**Purpose**: AI-optimized execution guide for Claude Code agents working with petstore-mcp

---

## 6a8 CRITICAL RULES (Check Every Task)

| Rule | Trigger | Action |
|------|---------|--------|
| **Check Guides First** | ANY task/prompt | Read relevant `.codemie/guides/*` BEFORE searching code |
| **Testing** | User says "test", "write tests", "run tests" | Only then add/run tests |
| **Git Ops** | User says "commit", "push", "PR", "branch" | Only then do git operations |
| **Python** | Any Python install/run command | Use `python3` (no `python`) |

---

## 4da GUIDE IMPORTS

| Category | Guide Path | Purpose |
|----------|------------|---------|
| Architecture | .codemie/guides/architecture/architecture.md | How this MCP server is structured |
| API | .codemie/guides/api/api-patterns.md | How tools map to outbound Petstore API calls |

---

## 26a TASK CLASSIFIER

| Category | User Intent / Purpose | Example Requests | P0 Guide | P1 Guide |
|----------|----------------------|------------------|----------|----------|
| **Architecture** | Understand/extend the MCP server structure | "Add a new tool", "Where should this code go?" | .codemie/guides/architecture/architecture.md | - |
| **API** | Change tool endpoints, models, or Petstore calls | "Add pet endpoint", "Change response schema" | .codemie/guides/api/api-patterns.md | - |

---

## 504 EXECUTION WORKFLOW

1. Parse request intent 6e0e0f
2. Read the relevant guide(s)
3. Locate the code using `file:line` hints
4. Implement minimal changes consistent with patterns
5. Validate (only run tests if user asked)

---

## 6e0e0f COMMANDS

| Task | Command | Notes |
|------|---------|-------|
| **Setup** | `python3 -m venv .venv && source .venv/bin/activate && python3 -m pip install -U pip && python3 -m pip install -e .` | Editable install |
| **Run** | `python3 main.py` | Starts FastMCP server |
| **Test** 26a | (none) | No tests in repo |

---

## 3d7e0f PROJECT CONTEXT

### Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.14.3 (local) |
| Framework | FastMCP | (pin in pyproject) |
| HTTP client | httpx | (pin in pyproject) |
| Validation | Pydantic | (pin in pyproject) |

### Project Structure

```
petstore_mcp/
4c4 main.py
4c1 .codemie/guides/
4c4 pyproject.toml
```

### Key Integrations

| Integration | Purpose | Guide |
|-------------|---------|-------|
| Swagger Petstore | Remote API used by tools | .codemie/guides/api/api-patterns.md |

---

## 527 TROUBLESHOOTING

| Symptom | Cause | Solution |
|---------|-------|----------|
| `python: command not found` | macOS env uses `python3` only | Use `python3 ...` |
| Import errors for `fastmcp/httpx/pydantic` | deps not installed | Create venv + `pip install -e .` |