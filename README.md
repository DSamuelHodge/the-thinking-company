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

Note: The JIRA tools require the `JIRA_BASE_URL`, `JIRA_USERNAME`, and `JIRA_API_TOKEN` environment variables to be set. If you don't set them, the JSON runner will return an authentication error.

## Troubleshooting

### Verification Script Output

The `verify_connectors.py` script exercises all connectors with read-only calls to verify they are callable and connected:

```bash
python verify_connectors.py
```

**Expected Output Analysis:**

- **JIRA**: Shows "Fallback Error: 410" → JIRA API deprecated the old endpoint and suggests migration to `/rest/api/3/search/jql`. The connector tries the new endpoint first and falls back gracefully. This is normal.
  - **Fix**: Ensure `JIRA_BASE_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` are set in `.env` and that the account has permissions. The code already handles the migration correctly.

- **Confluence**: Shows "Error: 404" → The search endpoint was not found or the credentials/permissions are incorrect.
  - **Fix**: Verify `CONFLUENCE_BASE_URL` (e.g., `https://your-domain.atlassian.net`), `CONFLUENCE_USERNAME`, and `CONFLUENCE_API_TOKEN` in `.env`. Ensure your Confluence instance is accessible and that your API token has read permissions.

- **Cal.com**: Shows "Error: 401 - No apiKey provided" → The API key is not recognized.
  - **Fix**: Verify `CAL_API_KEY` is set in `.env` and is a valid Cal.com API key. Check Cal.com documentation for the correct API key format and endpoint. The connector now includes both Bearer and x-api-key headers for compatibility.

- **Resend**: Shows "Error: missing or invalid recipient (to)" → The recipient email is not set.
  - **Fix**: Set `RECIPIENT` in `.env` to a valid email address (e.g., `RECIPIENT=user@example.com`), or ensure the `verify_connectors.py` script passes a valid `to` parameter. Note: The `send_email` function will attempt to send an actual email; use a test email address or verify RESEND_API_KEY is set to avoid unexpected email sends.

### Running Postman Tests

1. Start the JSON runner:
   ```powershell
   python run_jira_json.py
   ```

2. In Postman, import the collection:
   - File → Import → Select `postman/mcp_connectors.postman_collection.json`

3. Set the environment variables in Postman:
   - Click "Environments" → Select `postman/mcp_connectors.postman_environment.json` (or create/import)
   - Ensure `mcp_json_url` is set to `http://127.0.0.1:8001`

4. Run requests and observe test results:
   - Each request includes automated assertions (Postman Tests tab)
   - Tests verify expected HTTP status codes and response structure