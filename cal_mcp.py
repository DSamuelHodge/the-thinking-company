from fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Placeholder for API key - replace with your actual Cal.com API key
CAL_API_KEY = os.getenv("CAL_API_KEY")

mcp = FastMCP("Cal.com MCP Server")

@mcp.tool
def get_event_types() -> str:
    """Get list of event types from Cal.com."""
    if not CAL_API_KEY:
        raise ValueError('CAL_API_KEY is not set')

    url = "https://api.cal.com/v2/event-types"
    # Cal.com API v2 requires cal-api-version header
    headers = {
        "Authorization": CAL_API_KEY,
        "cal-api-version": "2024-08-06",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when calling Cal.com event-types: {exc}"

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def create_booking(event_type_id: int, start_time: str, attendee_email: str, attendee_name: str) -> str:
    """Create a booking on Cal.com."""
    if not CAL_API_KEY:
        raise ValueError('CAL_API_KEY is not set')

    url = "https://api.cal.com/v2/bookings"
    headers = {
        "Authorization": CAL_API_KEY,
        "cal-api-version": "2024-08-06",
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
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when creating Cal.com booking: {exc}"

    if response.status_code == 201:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

@mcp.tool
def get_availability(event_type_id: int, date_from: str, date_to: str) -> str:
    """Get availability for an event type."""
    if not CAL_API_KEY:
        raise ValueError('CAL_API_KEY is not set')

    url = f"https://api.cal.com/v2/event-types/{event_type_id}/availability"
    headers = {
        "Authorization": CAL_API_KEY,
        "cal-api-version": "2024-08-06",
        "Content-Type": "application/json"
    }
    params = {"dateFrom": date_from, "dateTo": date_to}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
    except requests.RequestException as exc:
        return f"Request exception when fetching Cal.com availability: {exc}"

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            return f"OK ({response.status_code}) but failed to decode JSON: {response.text}"
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()