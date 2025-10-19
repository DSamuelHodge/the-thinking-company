from fastmcp import FastMCP
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# Placeholders for credentials - replace with your actual values
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

def get_basic_auth_header(username: str | None, token: str | None) -> str:
    """Generate Basic Auth header value."""
    if not username or not token:
        raise ValueError("Username and token are required for authentication")
    credentials = f"{username}:{token}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"

mcp = FastMCP("JIRA MCP Server")

@mcp.tool
def search_issues(jql: str) -> str:
    """Search for JIRA issues using JQL query."""
    # New endpoint: /rest/api/3/search/jql expects a JSON body with `query`
    if not JIRA_BASE_URL:
        raise ValueError('JIRA_BASE_URL is not set')
    url = f"{JIRA_BASE_URL.rstrip('/')}/rest/api/3/search/jql"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": get_basic_auth_header(JIRA_USERNAME, JIRA_API_TOKEN)
    }
    payload = {"query": jql}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> str:
    """Create a new JIRA issue."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": get_basic_auth_header(JIRA_USERNAME, JIRA_API_TOKEN)
    }
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def get_issue(issue_key: str) -> str:
    """Get details of a JIRA issue."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    headers = {
        "Accept": "application/json",
        "Authorization": get_basic_auth_header(JIRA_USERNAME, JIRA_API_TOKEN)
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()