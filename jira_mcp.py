from fastmcp import FastMCP
import requests
import os

# Placeholders for credentials - replace with your actual values
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "https://your-domain.atlassian.net")
JIRA_USERNAME = os.getenv("JIRA_USERNAME", "your-email@example.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "your-api-token")

mcp = FastMCP("JIRA MCP Server")

@mcp.tool
def search_issues(jql: str) -> str:
    """Search for JIRA issues using JQL query."""
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {requests.auth._basic_auth_str(JIRA_USERNAME, JIRA_API_TOKEN)}"
    }
    params = {"jql": jql}
    response = requests.get(url, headers=headers, params=params)
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
        "Authorization": f"Basic {requests.auth._basic_auth_str(JIRA_USERNAME, JIRA_API_TOKEN)}"
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
        "Authorization": f"Basic {requests.auth._basic_auth_str(JIRA_USERNAME, JIRA_API_TOKEN)}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()