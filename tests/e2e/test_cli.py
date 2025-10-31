"""
E2E CLI tests using snapshot testing with syrupy.

Tests the browser CLI application with various URL schemes and captures
the output using snapshots for regression testing.
"""

from typer.testing import CliRunner
from browser.__main__ import app


runner = CliRunner()


class TestDataURLs:
    """Test data: URL scheme with various configurations."""

    def test_plain_text_data_url(self, snapshot):
        """Test plain text data URL."""
        result = runner.invoke(app, ["data:,Hello%20World"])
        assert result.output == snapshot

    def test_plain_text_with_charset(self, snapshot):
        """Test data URL with explicit charset."""
        result = runner.invoke(app, ["data:text/plain;charset=UTF-8,Hello"])
        assert result.output == snapshot

    def test_html_data_url(self, snapshot):
        """Test HTML data URL."""
        result = runner.invoke(app, ["data:text/html,<h1>Hello</h1>"])
        assert result.output == snapshot

    def test_base64_encoded_data_url(self, snapshot):
        """Test base64 encoded data URL."""
        # "Hello, World!" in base64
        result = runner.invoke(app, ["data:text/plain;base64,SGVsbG8sIFdvcmxkIQ=="])
        assert result.output == snapshot

    def test_empty_data_url(self, snapshot):
        """Test minimal/empty data URL."""
        result = runner.invoke(app, ["data:,"])
        assert result.output == snapshot

    def test_data_url_with_semicolon_in_content(self, snapshot):
        """Test data URL containing semicolon in the actual data."""
        result = runner.invoke(app, ["data:,foo;bar"])
        assert result.output == snapshot

    def test_data_url_multiline_html(self, snapshot):
        """Test data URL with multiline HTML content."""
        html = "<!DOCTYPE html><html><body><p>Line 1</p><p>Line 2</p></body></html>"
        result = runner.invoke(app, [f"data:text/html,{html}"])
        assert result.output == snapshot


class TestFileURLs:
    """Test file: URL scheme with local files."""

    def test_file_url_html(self, snapshot, fixtures_dir):
        """Test reading HTML file via file:// URL."""
        file_path = fixtures_dir / "sample.html"
        result = runner.invoke(app, [f"file://{file_path}"])
        assert result.output == snapshot

    def test_file_url_text(self, snapshot, fixtures_dir):
        """Test reading plain text file via file:// URL."""
        file_path = fixtures_dir / "sample.txt"
        result = runner.invoke(app, [f"file://{file_path}"])
        assert result.output == snapshot

    def test_file_url_with_localhost(self, snapshot, fixtures_dir):
        """Test file URL with explicit localhost."""
        file_path = fixtures_dir / "sample.txt"
        result = runner.invoke(app, [f"file://localhost{file_path}"])
        assert result.output == snapshot


class TestHTTPURLs:
    """Test HTTP URL scheme with mocked responses."""

    def test_http_simple_html(self, snapshot, mock_http_connection):
        """Test HTTP request returning simple HTML."""
        html = "<html><body><h1>Hello from HTTP</h1></body></html>"
        with mock_http_connection(html):
            result = runner.invoke(app, ["http://example.com/"])
        assert result.output == snapshot

    def test_http_plain_text(self, snapshot, mock_http_connection):
        """Test HTTP request returning plain text."""
        text = "This is plain text from HTTP server."
        with mock_http_connection(text):
            result = runner.invoke(app, ["http://example.com/page.txt"])
        assert result.output == snapshot

    def test_http_with_custom_port(self, snapshot, mock_http_connection):
        """Test HTTP URL with custom port."""
        content = "Response from port 8080"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://example.com:8080/"])
        assert result.output == snapshot

    def test_http_with_path(self, snapshot, mock_http_connection):
        """Test HTTP URL with path segments."""
        content = "Page content"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://example.com/path/to/page.html"])
        assert result.output == snapshot

    def test_http_with_query(self, snapshot, mock_http_connection):
        """Test HTTP URL with query string."""
        content = "Search results"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://example.com/search?q=test&lang=en"])
        assert result.output == snapshot

    def test_http_with_fragment(self, snapshot, mock_http_connection):
        """Test HTTP URL with fragment."""
        content = "Page with section"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://example.com/page#section"])
        assert result.output == snapshot


class TestHTTPSURLs:
    """Test HTTPS URL scheme with mocked responses."""

    def test_https_simple_html(self, snapshot, mock_http_connection):
        """Test HTTPS request returning simple HTML."""
        html = "<html><body><h1>Hello from HTTPS</h1></body></html>"
        with mock_http_connection(html):
            result = runner.invoke(app, ["https://example.com/"])
        assert result.output == snapshot

    def test_https_with_path_and_query(self, snapshot, mock_http_connection):
        """Test HTTPS URL with path and query parameters."""
        content = "Secure page content"
        with mock_http_connection(content):
            result = runner.invoke(app, ["https://api.example.com/v1/users?id=123"])
        assert result.output == snapshot


class TestHTTPRedirects:
    """Test HTTP redirect handling."""

    def test_http_redirect(self, snapshot, mock_http_response):
        """Test HTTP 301 redirect."""
        import unittest.mock
        from unittest.mock import patch

        # First response is a redirect
        redirect_response = mock_http_response(
            status_code=301,
            headers={"location": "http://example.com/new-location"},
            body="",
        )

        # Second response is the final content
        final_response = mock_http_response(
            status_code=200, body="Content after redirect"
        )

        mock_conn = unittest.mock.MagicMock()
        mock_conn.send.side_effect = [redirect_response, final_response]

        with patch("browser.protocols.create_connection", return_value=mock_conn):
            result = runner.invoke(app, ["http://example.com/old-location"])
        assert result.output == snapshot


class TestInvalidURLs:
    """Test error handling for invalid URLs."""

    def test_invalid_url_format(self, snapshot):
        """Test completely invalid URL format."""
        result = runner.invoke(app, ["not-a-valid-url"])
        assert result.output == snapshot
        assert result.exit_code != 0

    def test_missing_scheme(self, snapshot):
        """Test URL without scheme."""
        result = runner.invoke(app, ["example.com"])
        assert result.output == snapshot
        assert result.exit_code != 0

    def test_unsupported_scheme(self, snapshot):
        """Test URL with unsupported scheme."""
        result = runner.invoke(app, ["ftp://example.com/file.txt"])
        # This will fail during handling, not parsing
        # The error should be captured in the output
        assert result.output == snapshot


class TestEdgeCases:
    """Test edge cases and special URL formats."""

    def test_url_with_userinfo(self, snapshot, mock_http_connection):
        """Test HTTP URL with username and password."""
        content = "Authenticated content"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://user:pass@example.com/"])
        assert result.output == snapshot

    def test_url_with_ipv4_host(self, snapshot, mock_http_connection):
        """Test HTTP URL with IPv4 address."""
        content = "Response from IP"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://192.168.1.1/"])
        assert result.output == snapshot

    def test_url_with_ipv6_host(self, snapshot, mock_http_connection):
        """Test HTTP URL with IPv6 address."""
        content = "IPv6 response"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://[2001:db8::1]/"])
        assert result.output == snapshot

    def test_url_with_default_http_port(self, snapshot, mock_http_connection):
        """Test HTTP URL with explicit default port 80."""
        content = "Default port response"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://example.com:80/"])
        assert result.output == snapshot

    def test_url_with_default_https_port(self, snapshot, mock_http_connection):
        """Test HTTPS URL with explicit default port 443."""
        content = "HTTPS default port"
        with mock_http_connection(content):
            result = runner.invoke(app, ["https://example.com:443/"])
        assert result.output == snapshot

    def test_data_url_with_special_chars(self, snapshot):
        """Test data URL with special characters."""
        result = runner.invoke(app, ["data:,Special chars: !@#$%^&*()"])
        assert result.output == snapshot

    def test_empty_path_http_url(self, snapshot, mock_http_connection):
        """Test HTTP URL with no path (should use /)."""
        content = "Root page"
        with mock_http_connection(content):
            result = runner.invoke(app, ["http://example.com"])
        assert result.output == snapshot
