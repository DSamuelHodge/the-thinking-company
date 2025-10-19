import pytest
from unittest.mock import Mock, patch
import os
import sys

# Add parent directory to path to import mcp modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import confluence_mcp
from confluence_mcp import get_basic_auth_header


class TestConfluenceMCP:
    """Test suite for Confluence MCP connector."""

    @pytest.fixture
    def mock_env_vars(self, monkeypatch):
        """Set up mock environment variables."""
        monkeypatch.setenv("CONFLUENCE_BASE_URL", "https://test.atlassian.net")
        monkeypatch.setenv("CONFLUENCE_USERNAME", "test@example.com")
        monkeypatch.setenv("CONFLUENCE_API_TOKEN", "test-token-123")

    def test_get_basic_auth_header(self):
        """Test basic auth header generation."""
        header = get_basic_auth_header("user", "pass")
        assert header.startswith("Basic ")
        assert len(header) > 6

    def test_get_basic_auth_header_none_values(self):
        """Test basic auth header with None values."""
        with pytest.raises(ValueError, match="Username and token are required"):
            get_basic_auth_header(None, None)

    @patch('confluence_mcp.requests.get')
    def test_search_pages_success(self, mock_get, mock_env_vars):
        """Test successful Confluence page search."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {"id": "123", "title": "Test Page", "type": "page"}
            ]
        }
        mock_get.return_value = mock_response

        # Execute
        result = confluence_mcp.search_pages.fn("test query")

        # Assert
        assert result == {"results": [{"id": "123", "title": "Test Page", "type": "page"}]}
        mock_get.assert_called_once()

    @patch('confluence_mcp.requests.get')
    def test_search_pages_with_space_key(self, mock_get, mock_env_vars):
        """Test Confluence page search with space key."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        # Execute
        result = confluence_mcp.search_pages.fn("test query", space_key="DEV")

        # Assert
        assert result == {"results": []}
        # Verify the CQL query includes space filter
        call_args = mock_get.call_args
        assert "space = DEV" in str(call_args)

    @patch('confluence_mcp.requests.get')
    def test_search_pages_error(self, mock_get, mock_env_vars):
        """Test Confluence page search with error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.return_value = mock_response

        # Execute
        result = confluence_mcp.search_pages.fn("test query")

        # Assert
        assert "Error: 403" in result
        assert "Forbidden" in result

    @patch('confluence_mcp.requests.post')
    def test_create_page_success(self, mock_post, mock_env_vars):
        """Test successful Confluence page creation."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "456",
            "title": "New Page",
            "type": "page"
        }
        mock_post.return_value = mock_response

        # Execute
        result = confluence_mcp.create_page.fn("DEV", "New Page", "<p>Content</p>")

        # Assert
        assert result == {"id": "456", "title": "New Page", "type": "page"}
        mock_post.assert_called_once()

    @patch('confluence_mcp.requests.post')
    def test_create_page_error(self, mock_post, mock_env_vars):
        """Test Confluence page creation with error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Invalid space key"
        mock_post.return_value = mock_response

        # Execute
        result = confluence_mcp.create_page.fn("INVALID", "New Page", "<p>Content</p>")

        # Assert
        assert "Error: 400" in result
        assert "Invalid space key" in result

    @patch('confluence_mcp.requests.get')
    def test_get_page_success(self, mock_get, mock_env_vars):
        """Test successful get Confluence page."""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "789",
            "title": "Existing Page",
            "body": {
                "storage": {
                    "value": "<p>Page content</p>",
                    "representation": "storage"
                }
            }
        }
        mock_get.return_value = mock_response

        # Execute
        result = confluence_mcp.get_page.fn("789")

        # Assert
        assert result["id"] == "789"
        assert result["title"] == "Existing Page"
        assert "body" in result
        mock_get.assert_called_once()

    @patch('confluence_mcp.requests.get')
    def test_get_page_not_found(self, mock_get, mock_env_vars):
        """Test get Confluence page with not found error."""
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Page not found"
        mock_get.return_value = mock_response

        # Execute
        result = confluence_mcp.get_page.fn("999")

        # Assert
        assert "Error: 404" in result
        assert "Page not found" in result
