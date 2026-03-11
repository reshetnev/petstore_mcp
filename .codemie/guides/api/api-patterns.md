---
# API Patterns Guide

**Project**: petstore-mcp
**Stack**: Python + FastMCP + httpx + Pydantic
**Base URL**: `https://petstore3.swagger.io/api/v3`

---

## File Structure

| Purpose | Path |
|---------|------|
| Tool endpoints (MCP tools) | `main.py` |
| Validation + schemas | `main.py` (Pydantic models) |
| External HTTP calls | `main.py` (via `httpx.AsyncClient`) |

---

## Tool  External REST Call Pattern

This MCP server exposes tools that proxy to Swagger Petstore endpoints.

```python
# Source: main.py:40-50
async def find_pets_by_status(params: InputParams):
    inp: FindByStatusInput = params.input
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://petstore3.swagger.io/api/v3/pet/findByStatus",
            params={"status": inp.status},
        )
        response.raise_for_status()
        results = response.json()
    pets = [Pet(**data) for data in results]
    return FindByStatusOutput(pets=pets)
```

**To add a new Petstore-backed tool, replicate this structure:**
1. Define input/output Pydantic models (see `main.py:26-31`).
2. Call the Petstore endpoint with `httpx.AsyncClient`.
3. `raise_for_status()` then map `response.json()` into Pydantic models.
4. Return an output schema instance.

---

## Validation Pattern

**Approach**: Pydantic request/response models.

```python
# Source: main.py:26-31
class FindByStatusInput(BaseModel):
    status: str  # Comma-separated string: "available", "pending", "sold"

class FindByStatusOutput(BaseModel):
    pets: List[Pet]
```

---

## Response Patterns

- **Success**: a typed Pydantic output object, e.g. `FindByStatusOutput(pets=[...])` (`main.py:50`).
- **Error**: HTTP errors are surfaced by `response.raise_for_status()` (`main.py:47`).

---

## Conventions

| Aspect | Convention Used |
|--------|-----------------|
| Tool naming | `resource/action` (e.g. `pet/findByStatus`) (`main.py:35`) |
| Async handling | `async def` + `httpx.AsyncClient()` (`main.py:40-46`) |
| External URL | Inline Petstore URL for now (`main.py:44`) |

---

## Quick Reference

| Task | Syntax | Example |
|------|--------|---------|
| Define tool | `@tool(name=..., input=..., output=...)` | `main.py:34-39` |
| Call Petstore | `await client.get(url, params=...)` | `main.py:43-46` |
| Return typed output | `return OutputModel(...)` | `main.py:50` |
