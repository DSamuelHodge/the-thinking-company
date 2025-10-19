from fastmcp import FastMCP
import requests
import os

# Placeholder for API key - replace with your actual Cal.com API key
CAL_API_KEY = os.getenv("CAL_API_KEY")

mcp = FastMCP("Cal.com MCP Server")

@mcp.tool
def get_event_types() -> str:
    """Get list of event types from Cal.com."""
    url = "https://api.cal.com/v1/event-types"
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def create_booking(event_type_id: int, start_time: str, attendee_email: str, attendee_name: str) -> str:
    """Create a booking on Cal.com."""
    url = "https://api.cal.com/v1/bookings"
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "eventTypeId": event_type_id,
        "start": start_time,  # ISO 8601 format
        "responses": {
            "email": attendee_email,
            "name": attendee_name
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def get_availability(event_type_id: int, date_from: str, date_to: str) -> str:
    """Get availability for an event type."""
    url = f"https://api.cal.com/v1/event-types/{event_type_id}/availability"
    headers = {
        "Authorization": f"Bearer {CAL_API_KEY}",
        "Content-Type": "application/json"
    }
    params = {"dateFrom": date_from, "dateTo": date_to}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()