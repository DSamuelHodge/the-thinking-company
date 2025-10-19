import pytest
from unittest.mock import Mock, patch
import os
import sys

# Add parent directory to path to import mcp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import resend_mcp


class TestResendMCP:
    """Test suite for Resend MCP connector."""

    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Set up mock environment variables."""
        monkeypatch.setenv("RESEND_API_KEY", "re_test_key_123")

    @patch('resend_mcp.requests.post')
    def test_send_email_success(self, mock_post, mock_env_vars):
        """Test successful email send."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "email_12345",
            "from": "onboarding@resend.dev",
            "to": ["test@example.com"],
            "created_at": "2025-10-18T10:00:00.000Z"
        }
        mock_post.return_value = mock_response

        # Execute
        result = resend_mcp.send_email.fn(
            to="test@example.com",
            subject="Test Email",
            html="<p>Test content</p>"
        )

        # Assert
        assert result["id"] == "email_12345"
        assert result["to"] == ["test@example.com"]
        mock_post.assert_called_once()

    @patch('resend_mcp.requests.post')
    def test_send_email_custom_from(self, mock_post, mock_env_vars):
        """Test email send with custom from address."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "email_67890",
            "from": "custom@example.com",
            "to": ["recipient@example.com"]
        }
        mock_post.return_value = mock_response

        # Execute
        result = resend_mcp.send_email.fn(
            to="recipient@example.com",
            subject="Test Email",
            html="<p>Test content</p>",
            from_email="custom@example.com"
        )

        # Assert
        assert result["from"] == "custom@example.com"
        mock_post.assert_called_once()
        # Verify the from address was passed in the payload
        call_args = mock_post.call_args
        assert call_args.kwargs["json"]["from"] == "custom@example.com"

    @patch('resend_mcp.requests.post')
    def test_send_email_error_unauthorized(self, mock_post, mock_env_vars):
        """Test email send with unauthorized error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Invalid API key"
        mock_post.return_value = mock_response

        # Execute
        result = resend_mcp.send_email.fn(
            to="test@example.com",
            subject="Test Email",
            html="<p>Test content</p>"
        )

        # Assert
        assert "Error: 401" in result
        assert "Invalid API key" in result

    @patch('resend_mcp.requests.post')
    def test_send_email_error_rate_limit(self, mock_post, mock_env_vars):
        """Test email send with rate limit error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_post.return_value = mock_response

        # Execute
        result = resend_mcp.send_email.fn(
            to="test@example.com",
            subject="Test Email",
            html="<p>Test content</p>"
        )

        # Assert
        assert "Error: 429" in result
        assert "Rate limit exceeded" in result

    @patch('resend_mcp.requests.post')
    def test_send_email_error_bad_request(self, mock_post, mock_env_vars):
        """Test email send with bad request error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Invalid email format"
        mock_post.return_value = mock_response

        # Execute
        result = resend_mcp.send_email.fn(
            to="invalid-email",
            subject="Test Email",
            html="<p>Test content</p>"
        )

        # Assert
        assert "Error: 400" in result
        assert "Invalid email format" in result
