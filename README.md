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


## Running Tests

This project uses `pytest` for testing. To run all tests:

```bash
pytest
```

## Test Coverage

Test coverage is measured using `pytest-cov`.

### Install Coverage Tools

If you haven't already, install `pytest-cov`:

```bash
pip install pytest-cov
```

### Run Tests with Coverage

To run all tests and generate a coverage report (including an HTML report):

```bash
pytest --cov=./ --cov-report=html --cov-report=term-missing -q
```

### View the Coverage Report

After running the above command, an HTML coverage report will be generated in the `htmlcov` directory. To view it:

- **On Windows:**
   ```powershell
   Start-Process htmlcov\index.html
   ```
- **On macOS:**
   ```bash
   open htmlcov/index.html
   ```
- **On Linux:**
   ```bash
   xdg-open htmlcov/index.html
   ```

This will open a detailed, interactive coverage report in your default web browser.

## Testing MCP servers with Postman

FastMCP supports multiple transports. The default 'streamable-http' transport is optimized for streaming responses and uses text/event-stream. When using a streaming transport, clients must send an Accept header that includes both "application/json" and "text/event-stream". Postman doesn't automatically set this header, which can cause the "Not Acceptable" error:

```json
{
   "jsonrpc": "2.0",
   "id": "server-error",
   "error": {
      "code": -32600,
      "message": "Not Acceptable: Client must accept both application/json and text/event-stream"
   }
}
```

To call the streamable endpoint from Postman, add an explicit header:

Key: Accept
Value: application/json, text/event-stream

Or, use the included non-streaming JSON endpoint which is easier to test with Postman. Start the JSON runner:

```powershell
# Port 8001
python run_jira_json.py
```

Then send a POST to:

```
http://127.0.0.1:8001/mcp-json
```

Example request body (JSON):

```json
{
   "tool": "search_issues",
   "args": {
      "jql": "project = TEST"
   }
}
```

The response will be a JSON object containing either a "result" or an "error" field.