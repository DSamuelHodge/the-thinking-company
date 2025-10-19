from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn
import json

from jira_mcp import mcp
from fastmcp.exceptions import NotFoundError
from dotenv import load_dotenv
load_dotenv()

app = Starlette()


@app.route('/mcp-json', methods=['POST'])
async def handle_mcp(request: Request):
    """Accept a JSON body with 'tool' and 'args', run the tool, return JSON result.

    Example request body:
    {"tool": "search_issues", "args": {"jql": "project = TEST"}}
    """
    data = await request.json()
    tool_name = data.get('tool')
    args = data.get('args', {}) or {}
    try:
        tool = await mcp.get_tool(tool_name)
    except NotFoundError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    import inspect, asyncio
    try:
        # For FastMCP tools, call the underlying function (tool.fn).
        # It may be a coroutine (async) or a regular function.
        # FastMCP FunctionTool exposes the callable at `.fn`.
        fn = getattr(tool, 'fn', None) or (tool if callable(tool) else None)
        # Debug logging
        print('DEBUG: tool type=', type(tool), 'repr=', repr(tool))
        print('DEBUG: fn resolved type=', type(fn), 'callable=', callable(fn))
        # Validate required parameters if present
        params = getattr(tool, 'parameters', None) or {}
        required = params.get('required', []) if isinstance(params, dict) else []
        if required:
            missing = [r for r in required if r not in args]
            if missing:
                return JSONResponse({"error": f"Missing required parameter(s): {missing}"}, status_code=400)
        if fn is None or not callable(fn):
            return JSONResponse({"error": "Invalid tool function"}, status_code=500)
        if inspect.iscoroutinefunction(fn):
            result = await fn(**args)
        else:
            result = fn(**args)
        # Ensure result is JSON serializable
        try:
            json.dumps(result)
            return JSONResponse({"result": result})
        except TypeError:
            return JSONResponse({"result": str(result)})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == '__main__':
    import sys
    try:
        print("Starting JSON MCP endpoint on http://127.0.0.1:8001/mcp-json", file=sys.stderr)
        uvicorn.run(app, host='127.0.0.1', port=8001, log_level='info')
    except KeyboardInterrupt:
        print("\nShutting down...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)
