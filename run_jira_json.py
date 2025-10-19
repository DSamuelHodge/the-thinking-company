from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn
import json

from jira_mcp import mcp

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
    tool = mcp.get_tool(tool_name)
    if tool is None:
        return JSONResponse({"error": f"Tool '{tool_name}' not found"}, status_code=404)
    try:
        # For FastMCP tools, call the underlying function (tool.fn) synchronously
        result = tool.fn(**args)
        # Ensure result is JSON serializable
        try:
            json.dumps(result)
            return JSONResponse({"result": result})
        except TypeError:
            return JSONResponse({"result": str(result)})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)
