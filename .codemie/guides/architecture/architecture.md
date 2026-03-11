---
# Architecture Guide

**Project**: petstore-mcp
**Style**: Single-file service (Monolith)
**Language**: Python | **Framework**: FastMCP

---

## Architecture Overview

This repo is a minimal FastMCP server that exposes tools backed by the Swagger Petstore API.

```
FastMCP Server (main.py)
   includes tool(s)
        tool handler
             validates input (Pydantic)
             calls external HTTP API (httpx)
             maps JSON -> Pydantic models
             returns typed output schema
```

**Key Decision**: Keep everything in `main.py` for simplicity (single tool, minimal surface area).

---

## Component Structure

```
petstore_mcp/
 main.py              # FastMCP server + tool(s) + schemas
 pyproject.toml        # deps + entrypoint script
 requirements.txt      # deps (alternative install)
 .codemie/guides/       # AI-oriented guides (this folder)
```

---

## Design Patterns Detected

| Pattern | Usage | Location |
|---------|-------|----------|
| Single entrypoint module | Server, tool(s), and models in one file | `main.py:1-58` |
| Schema-first tool design | Input/output are Pydantic models referenced by tool decorator | `main.py:26-39` |
| External API adapter | Tool handler wraps Petstore REST call | `main.py:42-50` |

### Primary Pattern: Schema-first tool definition

```python
# Source: main.py:34-50
@tool(
    name="pet/findByStatus",
    description="Finds pets by status (available, pending, sold). Returns a list of pets.",
    input=FindByStatusInput,
    output=FindByStatusOutput,
)
async def find_pets_by_status(params: InputParams):
    inp: FindByStatusInput = params.input
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://petstore3.swagger.io/api/v3/pet/findByStatus",
            params={"status": inp.status},
        )
        results = response.json()
    return FindByStatusOutput(pets=[Pet(**data) for data in results])
```

---

## Data Flow

**Example flow** (`pet/findByStatus`):
1. Tool invoked with `FindByStatusInput` (`main.py:26-28`)
2. Handler performs outbound GET to Petstore (`main.py:42-46`)
3. Response JSON list is parsed into `Pet` models (`main.py:49`)
4. Returns `FindByStatusOutput(pets=[...])` (`main.py:50`)

---

## Adding New Features

### To add a new tool

1. Add/extend Pydantic models (input/output) near the existing schemas (`main.py:24-31`).
2. Implement a new async function decorated with `@tool(...)` similar to `find_pets_by_status` (`main.py:34-50`).
3. Register it in `server.include_tools([...])` (`main.py:54-55`).

---

## Boundaries Summary

|  DO |  DON'T |
|-------|----------|
| Keep tool contracts explicit via Pydantic input/output models | Return raw dicts/lists when a typed output schema exists |
| Keep outbound API calls inside tool handlers | Scatter Petstore HTTP calls across unrelated modules |
| Use `file:line` locations when referencing code | Copy large blocks of code into guides |

---

## Quick Reference

| Need | Location | Pattern |
|------|----------|---------|
| Entry point | `main.py:1` | Single module |
| Tool registration | `main.py:54-55` | `server.include_tools([...])` |
| Tool definition | `main.py:34-39` | `@tool(..., input=..., output=...)` |
