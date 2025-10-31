import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

# Add the project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def fixtures_dir():
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_http_response():
    """Factory fixture to create mock HTTP responses."""
    from browser.protocols.http.response import HttpResponse
    from browser.protocols.http.request import HttpRequest

    def _create_response(
        status_code: int = 200,
        status_message: str = "OK",
        headers: dict[str, str] | None = None,
        body: str = "",
        version: str = "HTTP/1.1",
    ):
        """Create a mock HttpResponse object."""
        request = HttpRequest(
            method="GET",
            path="/",
            headers={"Host": "example.com"},
            version="1.1",
        )
        return HttpResponse(
            version=version,
            status_code=status_code,
            status_message=status_message,
            headers=headers or {},
            body=body,
            request=request,
        )

    return _create_response


@pytest.fixture
def mock_http_connection(mock_http_response):
    """Fixture to mock HTTP/HTTPS connections."""

    def _mock_connection(
        response_body: str,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ):
        """
        Mock HTTP connection with specified response.

        Args:
            response_body: The body content to return
            status_code: HTTP status code (default: 200)
            headers: Response headers (default: empty dict)

        Returns:
            A context manager for the mock patch
        """
        response = mock_http_response(
            status_code=status_code, body=response_body, headers=headers or {}
        )

        # Create a mock that returns our response
        mock_conn = MagicMock()
        mock_conn.send.return_value = response

        # Patch both HTTP and HTTPS connection creation
        return patch("browser.protocols.create_connection", return_value=mock_conn)

    return _mock_connection
