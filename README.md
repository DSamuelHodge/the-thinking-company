# MCP Connectors for JIRA, Confluence, Resend, and Cal.com

This project provides MCP (Model Context Protocol) servers built with FastMCP for connecting to various APIs: JIRA, Confluence, Resend, and Cal.com. Each service has its own MCP server that exposes tools for interacting with the respective API.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables for credentials (see each section below).

3. Run the desired MCP server:
   ```bash
   python jira_mcp.py
   # or
   python confluence_mcp.py
   # or
   python resend_mcp.py
   # or
   python cal_mcp.py
   ```

## JIRA MCP Server

**File:** `jira_mcp.py`

**Environment Variables:**
- `JIRA_BASE_URL`: Your JIRA instance URL (e.g., https://your-domain.atlassian.net)
- `JIRA_USERNAME`: Your JIRA email/username
- `JIRA_API_TOKEN`: Your JIRA API token

**Tools:**
- `search_issues(jql: str)`: Search for JIRA issues using JQL
- `create_issue(project_key: str, summary: str, description: str, issue_type: str = "Task")`: Create a new JIRA issue
- `get_issue(issue_key: str)`: Get details of a JIRA issue

**API Documentation:** https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Overview: The Jira REST API enables you to interact with Jira programmatically. Use this API to build apps, script interactions with Jira, or develop any other type of integration.
- Authentication: Supports basic auth, OAuth 2.0, Forge apps, Connect apps.
- Key features: Issues, projects, users, workflows, permissions, etc.

## Confluence MCP Server

**File:** `confluence_mcp.py`

**Environment Variables:**
- `CONFLUENCE_BASE_URL`: Your Confluence instance URL (e.g., https://your-domain.atlassian.net)
- `CONFLUENCE_USERNAME`: Your Confluence email/username
- `CONFLUENCE_API_TOKEN`: Your Confluence API token

**Tools:**
- `search_pages(query: str, space_key: str = None)`: Search for Confluence pages
- `create_page(space_key: str, title: str, content: str)`: Create a new Confluence page
- `get_page(page_id: str)`: Get content of a Confluence page

**API Documentation:** https://developer.atlassian.com/cloud/confluence/rest/v3/
- Overview: This is the reference for the Confluence Cloud REST API v2, with definitions and performance intended to be an improvement over v1.
- Authentication: Supports JWT, OAuth 2.0, basic auth.
- Key features: Pages, spaces, content, comments, attachments, etc.

## Resend MCP Server

**File:** `resend_mcp.py`

**Environment Variables:**
- `RESEND_API_KEY`: Your Resend API key

**Tools:**
- `send_email(to: str, subject: str, html: str, from_email: str = "onboarding@resend.dev")`: Send an email using Resend API

**API Documentation:** https://resend.com/docs/api-reference/introduction
- Overview: The Resend API is built on REST principles. We enforce HTTPS in every request to improve data security, integrity, and privacy.
- Base URL: https://api.resend.com
- Authentication: Bearer token in Authorization header
- Key features: Send emails, manage domains, webhooks, etc.

## Cal.com MCP Server

**File:** `cal_mcp.py`

**Environment Variables:**
- `CAL_API_KEY`: Your Cal.com API key

**Tools:**
- `get_event_types()`: Get list of event types from Cal.com
- `create_booking(event_type_id: int, start_time: str, attendee_email: str, attendee_name: str)`: Create a booking on Cal.com
- `get_availability(event_type_id: int, date_from: str, date_to: str)`: Get availability for an event type

**API Documentation:** https://cal.com/docs/api-reference/v2/introduction
- Overview: Introduction to Cal.com API v2 endpoints for scheduling and calendar management.
- Authentication: API key, OAuth client credentials, managed user access tokens.
- Key features: Bookings, event types, schedules, availability, webhooks, etc.

## Notes

- All credentials are loaded from environment variables with placeholder defaults.
- Replace the placeholder values with your actual credentials.
- Each MCP server runs independently and can be connected to an MCP client.
- The servers use FastMCP for simplified MCP implementation.

## Testing

This repository includes unit tests for each MCP connector using pytest. Tests mock HTTP requests and do not perform real network requests.

To run the tests:

```bash
pip install -r requirements.txt
pytest -v
```

What the tests cover:
- JIRA: search, create, and get issue behaviors, and auth header generation
- Confluence: search pages, create page, get page, and auth header generation
- Resend: sending emails and handling common errors
- Cal.com: event types, bookings, and availability responses

Notes:
- Tests use the `unittest.mock` module to patch `requests` calls and simulate API responses.
- Update or add tests in `tests/` when you add features or change behavior.