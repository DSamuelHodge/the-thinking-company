from fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Placeholder for API key - replace with your actual Resend API key
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

mcp = FastMCP("Resend MCP Server")

@mcp.tool
def send_email(to: str | None, subject: str, html: str, from_email: str = "onboarding@resend.dev") -> str:
    """Send an email using Resend API."""
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    # Ensure `to` is a single string. If None, try RECIPIENT from env.
    if not to:
        to = os.getenv('RECIPIENT')
    # Normalize recipient to a single string
    if isinstance(to, (list, tuple)):
        to_value = to[0] if to else None
    else:
        to_value = to

    if not to_value or not isinstance(to_value, str):
        return "Error: missing or invalid recipient (to). Set RECIPIENT env or pass a single string 'to' value."
    payload = {
        "from": from_email,
        "to": to_value,
        "subject": subject,
        "html": html
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when calling Resend: {exc}"

    # Resend may return 200 or 202 on success; accept both and decode JSON where possible
    if response.status_code in (200, 202):
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()