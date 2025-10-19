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
    if isinstance(to, (list, tuple)):
        to_value = to[0] if to else None
    else:
        to_value = to
    payload = {
        "from": from_email,
        "to": to_value,
        "subject": subject,
        "html": html
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()