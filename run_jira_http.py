from jira_mcp import mcp

if __name__ == '__main__':
    # Run the MCP server with HTTP transport on port 8000 under path /mcp
    mcp.run('streamable-http', host='127.0.0.1', port=8000, path='/mcp')
