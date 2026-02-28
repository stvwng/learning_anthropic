# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup
uv venv && source .venv/bin/activate && uv pip install -e .

# Run MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_document.py

# Run a specific test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

## Architecture

This is an MCP (Model Context Protocol) server that exposes document processing tools to AI assistants.

**Entry point**: `main.py` creates a `FastMCP` server instance and registers tools via `mcp.tool()(function_name)`.

**Tools directory** (`tools/`): Each module contains tool functions that get registered with the MCP server. Currently includes:
- `math.py` - Mathematical operations (add)
- `document.py` - Document conversion using markitdown library

**Tests**: Located in `tests/` with fixtures in `tests/fixtures/`.

## Adding New MCP Tools

1. Create a function in `tools/` with Pydantic `Field` for parameter descriptions:
```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Description of param1"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - Use case 1
    - Use case 2

    Examples:
    >>> my_tool("input")
    "output"
    """
    # Implementation
```

2. Register in `main.py`:
```python
from tools.my_module import my_tool
mcp.tool()(my_tool)
```

## Dependencies

- `mcp[cli]` - MCP server framework (FastMCP)
- `markitdown[docx,pdf]` - Document to markdown conversion
- `pydantic` - Parameter validation and descriptions
