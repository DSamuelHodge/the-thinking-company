import pytest
from unittest.mock import Mock, patch
import os
import sys

# Add parent directory to path to import mcp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import jira_mcp
from jira_mcp import get_basic_auth_header


class TestJiraMCP:
    """Test suite for JIRA MCP connector."""

    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Set up mock environment variables."""
        monkeypatch.setenv("JIRA_BASE_URL", "https://test.atlassian.net")
        monkeypatch.setenv("JIRA_USERNAME", "test@example.com")
        monkeypatch.setenv("JIRA_API_TOKEN", "test-token-123")

    def test_get_basic_auth_header(self):
        """Test basic auth header generation."""
        header = get_basic_auth_header("user", "pass")
        assert header.startswith("Basic ")
        assert len(header) > 6

    def test_get_basic_auth_header_none_username(self):
        """Test basic auth header with None username."""
        with pytest.raises(ValueError, match="Username and token are required"):
            get_basic_auth_header(None, "pass")

    def test_get_basic_auth_header_none_token(self):
        """Test basic auth header with None token."""
        with pytest.raises(ValueError, match="Username and token are required"):
            get_basic_auth_header("user", None)

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123"
    })
    @patch('jira_mcp.requests.get')
    def test_search_issues_success(self, mock_get):
        """Test successful JIRA issue search."""
        # Reload module to pick up environment variables
        import importlib
        importlib.reload(jira_mcp)
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "issues": [
                {"key": "TEST-1", "fields": {"summary": "Test Issue"}}
            ]
        }
        mock_get.return_value = mock_response

        # Execute - access the underlying function
        result = jira_mcp.search_issues.fn("project = TEST")

        # Assert
        assert result == {"issues": [{"key": "TEST-1", "fields": {"summary": "Test Issue"}}]}
        mock_get.assert_called_once()

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123"
    })
    @patch('jira_mcp.requests.get')
    def test_search_issues_error(self, mock_get):
        """Test JIRA issue search with error."""
        # Reload module to pick up environment variables
        import importlib
        importlib.reload(jira_mcp)
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        # Execute
        result = jira_mcp.search_issues.fn("project = TEST")

        # Assert
        assert "Error: 401" in result
        assert "Unauthorized" in result

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123"
    })
    @patch('jira_mcp.requests.post')
    def test_create_issue_success(self, mock_post):
        """Test successful JIRA issue creation."""
        # Reload module to pick up environment variables
        import importlib
        importlib.reload(jira_mcp)
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "key": "TEST-123",
            "id": "10000"
        }
        mock_post.return_value = mock_response

        # Execute
        result = jira_mcp.create_issue.fn("TEST", "Test Summary", "Test Description")

        # Assert
        assert result == {"key": "TEST-123", "id": "10000"}
        mock_post.assert_called_once()

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123"
    })
    @patch('jira_mcp.requests.post')
    def test_create_issue_error(self, mock_post):
        """Test JIRA issue creation with error."""
        # Reload module to pick up environment variables
        import importlib
        importlib.reload(jira_mcp)
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        # Execute
        result = jira_mcp.create_issue.fn("TEST", "Test Summary", "Test Description")

        # Assert
        assert "Error: 400" in result
        assert "Bad Request" in result

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123"
    })
    @patch('jira_mcp.requests.get')
    def test_get_issue_success(self, mock_get):
        """Test successful get JIRA issue."""
        # Reload module to pick up environment variables
        import importlib
        importlib.reload(jira_mcp)
        
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "key": "TEST-1",
            "fields": {
                "summary": "Test Issue",
                "status": {"name": "Open"}
            }
        }
        mock_get.return_value = mock_response

        # Execute
        result = jira_mcp.get_issue.fn("TEST-1")

        # Assert
        assert result["key"] == "TEST-1"
        assert result["fields"]["summary"] == "Test Issue"
        mock_get.assert_called_once()

    @patch.dict(os.environ, {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123"
    })
    @patch('jira_mcp.requests.get')
    def test_get_issue_not_found(self, mock_get):
        """Test get JIRA issue with not found error."""
        # Reload module to pick up environment variables
        import importlib
        importlib.reload(jira_mcp)
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Issue not found"
        mock_get.return_value = mock_response

        # Execute
        result = jira_mcp.get_issue.fn("TEST-999")

        # Assert
        assert "Error: 404" in result
        assert "Issue not found" in result
