from fastmcp import FastMCP
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

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
    if not CONFLUENCE_BASE_URL or CONFLUENCE_BASE_URL == "https://your-domain.atlassian.net":
        raise ValueError('CONFLUENCE_BASE_URL is not set or using placeholder')
    if not CONFLUENCE_USERNAME or CONFLUENCE_USERNAME == "your-email@example.com":
        raise ValueError('CONFLUENCE_USERNAME is not set or using placeholder')
    if not CONFLUENCE_API_TOKEN or CONFLUENCE_API_TOKEN == "your-api-token":
        raise ValueError('CONFLUENCE_API_TOKEN is not set or using placeholder')

    url = f"{CONFLUENCE_BASE_URL.rstrip('/')}/rest/api/content/search"
    headers = {
        "Accept": "application/json",
        "Authorization": get_basic_auth_header(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
    }
    params = {"cql": f"text ~ '{query}'" + (f" and space = {space_key}" if space_key else "")}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when calling Confluence search: {exc}"

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def create_page(space_key: str, title: str, content: str) -> str:
    """Create a new Confluence page."""
    if not CONFLUENCE_BASE_URL or CONFLUENCE_BASE_URL == "https://your-domain.atlassian.net":
        raise ValueError('CONFLUENCE_BASE_URL is not set or using placeholder')
    if not CONFLUENCE_USERNAME or CONFLUENCE_USERNAME == "your-email@example.com":
        raise ValueError('CONFLUENCE_USERNAME is not set or using placeholder')
    if not CONFLUENCE_API_TOKEN or CONFLUENCE_API_TOKEN == "your-api-token":
        raise ValueError('CONFLUENCE_API_TOKEN is not set or using placeholder')

    url = f"{CONFLUENCE_BASE_URL.rstrip('/')}/rest/api/content"
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
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when creating Confluence page: {exc}"

    if response.status_code in (200, 201):
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def get_page(page_id: str) -> str:
    """Get content of a Confluence page."""
    if not CONFLUENCE_BASE_URL or CONFLUENCE_BASE_URL == "https://your-domain.atlassian.net":
        raise ValueError('CONFLUENCE_BASE_URL is not set or using placeholder')
    if not CONFLUENCE_USERNAME or CONFLUENCE_USERNAME == "your-email@example.com":
        raise ValueError('CONFLUENCE_USERNAME is not set or using placeholder')
    if not CONFLUENCE_API_TOKEN or CONFLUENCE_API_TOKEN == "your-api-token":
        raise ValueError('CONFLUENCE_API_TOKEN is not set or using placeholder')

    url = f"{CONFLUENCE_BASE_URL.rstrip('/')}/rest/api/content/{page_id}?expand=body.storage"
    headers = {
        "Accept": "application/json",
        "Authorization": get_basic_auth_header(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when fetching Confluence page {page_id}: {exc}"

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()