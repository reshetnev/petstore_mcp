# petstore_mcp

FastMCP server exposing one tool: `pet/findByStatus`.

The tool calls the Swagger Petstore API endpoint:
`GET https://petstore3.swagger.io/api/v3/pet/findByStatus`
and returns typed `Pet` objects.

## Tool

- **Name:** `pet/findByStatus`
- **Input:**
  - `status` (`string`) - pet status filter (`available`, `pending`, `sold`)
- **Output:**
  - `pets` (`Pet[]`) - list of matching pets

## Project Structure

- `main.py` - FastMCP server and tool implementation
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.10+
- Packages:
  - `fastmcp`
  - `pydantic`
  - `httpx`

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python3 main.py
```

This starts the MCP server and registers `pet/findByStatus`.

## Notes

- The tool is asynchronous and uses `httpx.AsyncClient`.
- `status` is passed through to the Petstore API as a query parameter.
