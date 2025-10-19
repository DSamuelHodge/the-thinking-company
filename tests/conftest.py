import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture(scope="session")
def test_env_vars():
    """Provide test environment variables for all tests."""
    return {
        "JIRA_BASE_URL": "https://test.atlassian.net",
        "JIRA_USERNAME": "test@example.com",
        "JIRA_API_TOKEN": "test-token-123",
        "CONFLUENCE_BASE_URL": "https://test.atlassian.net",
        "CONFLUENCE_USERNAME": "test@example.com",
        "CONFLUENCE_API_TOKEN": "test-token-123",
        "RESEND_API_KEY": "re_test_key_123",
        "CAL_API_KEY": "cal_live_test_key_123"
    }
