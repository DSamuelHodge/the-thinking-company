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
    # Prefer the new JQL search endpoint, but fall back to the older search endpoint
    if not JIRA_BASE_URL:
        raise ValueError('JIRA_BASE_URL is not set')

    auth_header = get_basic_auth_header(JIRA_USERNAME, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": auth_header
    }

    # Try the new POST-based JQL endpoint first
    post_url = f"{JIRA_BASE_URL.rstrip('/')}/rest/api/3/search/jql"
    post_payload = {"query": jql}
    try:
        resp = requests.post(post_url, headers=headers, json=post_payload, timeout=20)
    except requests.RequestException as exc:
        return f"Request error when calling {post_url}: {exc}"

    if resp.status_code == 200:
        try:
            return resp.json()
        except ValueError:
            return f"OK ({resp.status_code}) but failed to decode JSON: {resp.text}"

    # If the POST call indicates the endpoint is removed/deprecated or payload invalid,
    # try falling back to the traditional search endpoint which accepts a jql query param.
    # Examples of statuses to try fallback on: 410 (gone), 400 (bad request), 404 (not found)
    if resp.status_code in (410, 400, 404):
        get_url = f"{JIRA_BASE_URL.rstrip('/')}/rest/api/3/search"
        try:
            params = {"jql": jql}
            get_headers = {"Accept": "application/json", "Authorization": auth_header}
            get_resp = requests.get(get_url, headers=get_headers, params=params, timeout=20)
        except requests.RequestException as exc:
            return f"Request error when calling fallback {get_url}: {exc}"

        if get_resp.status_code == 200:
            try:
                return get_resp.json()
            except ValueError:
                return f"OK ({get_resp.status_code}) but failed to decode JSON: {get_resp.text}"
        else:
            return f"Fallback Error: {get_resp.status_code} - {get_resp.text}"

    # Otherwise return the original POST response as an error string
    return f"Error: {resp.status_code} - {resp.text}"

@mcp.tool
def create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> str:
    """Create a new JIRA issue."""
    if not JIRA_BASE_URL:
        raise ValueError('JIRA_BASE_URL is not set')

    url = f"{JIRA_BASE_URL.rstrip('/')}/rest/api/3/issue"
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
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when creating issue: {exc}"

    if response.status_code == 201:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def get_issue(issue_key: str) -> str:
    """Get details of a JIRA issue."""
    if not JIRA_BASE_URL:
        raise ValueError('JIRA_BASE_URL is not set')

    url = f"{JIRA_BASE_URL.rstrip('/')}/rest/api/3/issue/{issue_key}"
    headers = {
        "Accept": "application/json",
        "Authorization": get_basic_auth_header(JIRA_USERNAME, JIRA_API_TOKEN)
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when fetching issue {issue_key}: {exc}"

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()