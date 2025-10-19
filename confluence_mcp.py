from fastmcp import FastMCP
import requests
import os
import base64

# Placeholders for credentials - replace with your actual values
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL", "https://your-domain.atlassian.net")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME", "your-email@example.com")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN", "your-api-token")

def get_basic_auth_header(username: str | None, token: str | None) -> str:
    """Generate Basic Auth header value."""
    if not username or not token:
        raise ValueError("Username and token are required for authentication")
    credentials = f"{username}:{token}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"

mcp = FastMCP("Confluence MCP Server")

@mcp.tool
def search_pages(query: str, space_key: str | None = None) -> str:
    """Search for Confluence pages."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/search"
    headers = {
        "Accept": "application/json",
        "Authorization": get_basic_auth_header(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
    }
    params = {"cql": f"text ~ '{query}'" + (f" and space = {space_key}" if space_key else "")}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def create_page(space_key: str, title: str, content: str) -> str:
    """Create a new Confluence page."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": get_basic_auth_header(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
    }
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def get_page(page_id: str) -> str:
    """Get content of a Confluence page."""
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    headers = {
        "Accept": "application/json",
        "Authorization": get_basic_auth_header(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()