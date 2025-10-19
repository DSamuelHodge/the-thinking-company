import pytest
from unittest.mock import Mock, patch
import os
import sys

# Add parent directory to path to import mcp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cal_mcp


class TestCalMCP:
    """Test suite for Cal.com MCP connector."""

    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Set up mock environment variables."""
        monkeypatch.setenv("CAL_API_KEY", "cal_live_test_key_123")

    @patch('cal_mcp.requests.get')
    def test_get_event_types_success(self, mock_get, mock_env_vars):
        """Test successful get event types."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "event_types": [
                {"id": 1, "title": "30 Min Meeting", "length": 30},
                {"id": 2, "title": "60 Min Meeting", "length": 60}
            ]
        }
        mock_get.return_value = mock_response

        # Execute
        result = cal_mcp.get_event_types.fn()

        # Assert
        assert "event_types" in result
        assert len(result["event_types"]) == 2
        mock_get.assert_called_once()

    @patch('cal_mcp.requests.get')
    def test_get_event_types_error(self, mock_get, mock_env_vars):
        """Test get event types with error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        # Execute
        result = cal_mcp.get_event_types.fn()

        # Assert
        assert "Error: 401" in result
        assert "Unauthorized" in result

    @patch('cal_mcp.requests.post')
    def test_create_booking_success(self, mock_post, mock_env_vars):
        """Test successful booking creation."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "booking_123",
            "eventTypeId": 1,
            "startTime": "2025-10-20T10:00:00Z",
            "attendees": [
                {"email": "attendee@example.com", "name": "John Doe"}
            ]
        }
        mock_post.return_value = mock_response

        # Execute
        result = cal_mcp.create_booking.fn(
            event_type_id=1,
            start_time="2025-10-20T10:00:00Z",
            attendee_email="attendee@example.com",
            attendee_name="John Doe"
        )

        # Assert
        assert result["id"] == "booking_123"
        assert result["eventTypeId"] == 1
        mock_post.assert_called_once()

    @patch('cal_mcp.requests.post')
    def test_create_booking_error(self, mock_post, mock_env_vars):
        """Test booking creation with error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Time slot not available"
        mock_post.return_value = mock_response

        # Execute
        result = cal_mcp.create_booking.fn(
            event_type_id=1,
            start_time="2025-10-20T10:00:00Z",
            attendee_email="attendee@example.com",
            attendee_name="John Doe"
        )

        # Assert
        assert "Error: 400" in result
        assert "Time slot not available" in result

    @patch('cal_mcp.requests.get')
    def test_get_availability_success(self, mock_get, mock_env_vars):
        """Test successful get availability."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "slots": [
                {"time": "2025-10-20T09:00:00Z", "available": True},
                {"time": "2025-10-20T10:00:00Z", "available": True},
                {"time": "2025-10-20T11:00:00Z", "available": False}
            ]
        }
        mock_get.return_value = mock_response

        # Execute
        result = cal_mcp.get_availability.fn(
            event_type_id=1,
            date_from="2025-10-20",
            date_to="2025-10-21"
        )

        # Assert
        assert "slots" in result
        assert len(result["slots"]) == 3
        mock_get.assert_called_once()

    @patch('cal_mcp.requests.get')
    def test_get_availability_error(self, mock_get, mock_env_vars):
        """Test get availability with error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Event type not found"
        mock_get.return_value = mock_response

        # Execute
        result = cal_mcp.get_availability.fn(
            event_type_id=999,
            date_from="2025-10-20",
            date_to="2025-10-21"
        )

        # Assert
        assert "Error: 404" in result
        assert "Event type not found" in result

    @patch('cal_mcp.requests.get')
    def test_get_availability_params(self, mock_get, mock_env_vars):
        """Test get availability with correct parameters."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"slots": []}
        mock_get.return_value = mock_response

        # Execute
        cal_mcp.get_availability.fn(
            event_type_id=5,
            date_from="2025-10-25",
            date_to="2025-10-26"
        )

        # Assert
        call_args = mock_get.call_args
        # Verify URL contains event type id
        assert "/event-types/5/availability" in call_args[0][0]
        # Verify params contain date range
        assert call_args.kwargs["params"]["dateFrom"] == "2025-10-25"
        assert call_args.kwargs["params"]["dateTo"] == "2025-10-26"
