from fastmcp import FastMCP
import requests
import os

# Placeholder for API key - replace with your actual Resend API key
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "your-resend-api-key")

mcp = FastMCP("Resend MCP Server")

@mcp.tool
def send_email(to: str, subject: str, html: str, from_email: str = "onboarding@resend.dev") -> str:
    """Send an email using Resend API."""
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": from_email,
        "to": [to],
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