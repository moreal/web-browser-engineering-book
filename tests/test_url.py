import pytest
from browser.url import Url, DataUrl


class TestHTTPURLParsing:
    """Test HTTP URL parsing."""

    def test_http_basic(self):
        """Test basic HTTP URL parsing."""
        url = Url.parse("http://example.com/")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port is None
        assert url.path == "/"
        assert url.query is None
        assert url.fragment is None

    def test_http_with_port(self):
        """Test HTTP URL with explicit port."""
        url = Url.parse("http://example.com:8080/")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port == 8080
        assert url.path == "/"
        assert url.query is None
        assert url.fragment is None

    def test_http_with_path(self):
        """Test HTTP URL with path."""
        url = Url.parse("http://example.com/path/to/resource")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port is None
        assert url.path == "/path/to/resource"
        assert url.query is None
        assert url.fragment is None

    def test_http_with_query(self):
        """Test HTTP URL with query string."""
        url = Url.parse("http://example.com/search?q=test&page=1")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port is None
        assert url.path == "/search"
        assert url.query == "q=test&page=1"
        assert url.fragment is None

    def test_http_with_fragment(self):
        """Test HTTP URL with fragment."""
        url = Url.parse("http://example.com/page#section")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port is None
        assert url.path == "/page"
        assert url.query is None
        assert url.fragment == "section"

    def test_http_complete_url(self):
        """Test HTTP URL with all components."""
        url = Url.parse(
            "http://example.com:8080/path/to/page?key=value&foo=bar#section"
        )
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port == 8080
        assert url.path == "/path/to/page"
        assert url.query == "key=value&foo=bar"
        assert url.fragment == "section"

    def test_http_with_subdomain(self):
        """Test HTTP URL with subdomain."""
        url = Url.parse("http://www.sub.example.com/page")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "www.sub.example.com"
        assert url.path == "/page"

    def test_http_with_hyphen_in_host(self):
        """Test HTTP URL with hyphen in hostname."""
        url = Url.parse("http://my-example-site.com/")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "my-example-site.com"
        assert url.path == "/"

    def test_http_with_numbers_in_host(self):
        """Test HTTP URL with numbers in hostname."""
        url = Url.parse("http://example123.com/")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example123.com"
        assert url.path == "/"

    def test_http_with_empty_query(self):
        """Test HTTP URL with empty query string."""
        url = Url.parse("http://example.com/page?")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.path == "/page"
        assert url.query == ""
        assert url.fragment is None

    def test_http_with_empty_fragment(self):
        """Test HTTP URL with empty fragment."""
        url = Url.parse("http://example.com/page#")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.path == "/page"
        assert url.query is None
        assert url.fragment == ""

    def test_http_with_query_and_fragment(self):
        """Test HTTP URL with both query and fragment."""
        url = Url.parse("http://example.com/page?key=value#section")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.path == "/page"
        assert url.query == "key=value"
        assert url.fragment == "section"

    def test_http_with_special_chars_in_fragment(self):
        """Test HTTP URL with special characters in fragment."""
        url = Url.parse("http://example.com/page#section-1.2")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.path == "/page"
        assert url.fragment == "section-1.2"

    def test_http_with_standard_port(self):
        """Test HTTP URL with standard port 80."""
        url = Url.parse("http://example.com:80/")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.port == 80

    def test_http_with_high_port_number(self):
        """Test HTTP URL with high port number."""
        url = Url.parse("http://example.com:65535/")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.port == 65535

    def test_http_without_path_defaults_to_root(self):
        """Test that HTTP URL without path defaults to '/'."""
        url = Url.parse("http://example.com")
        assert url.path is None

    def test_http_with_query_no_path(self):
        """Test HTTP URL with query but no explicit path."""
        url = Url.parse("http://example.com?query=value")
        assert url.path is None
        assert url.query == "query=value"


class TestHTTPSURLParsing:
    """Test HTTPS URL parsing."""

    def test_https_basic(self):
        """Test basic HTTPS URL parsing."""
        url = Url.parse("https://secure.example.com/")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "secure.example.com"
        assert url.port is None
        assert url.path == "/"
        assert url.query is None
        assert url.fragment is None

    def test_https_with_port(self):
        """Test HTTPS URL with explicit port."""
        url = Url.parse("https://secure.example.com:8443/")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "secure.example.com"
        assert url.port == 8443
        assert url.path == "/"
        assert url.query is None
        assert url.fragment is None

    def test_https_with_path(self):
        """Test HTTPS URL with path."""
        url = Url.parse("https://api.example.com/v1/users/123")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "api.example.com"
        assert url.port is None
        assert url.path == "/v1/users/123"
        assert url.query is None
        assert url.fragment is None

    def test_https_with_query(self):
        """Test HTTPS URL with query string."""
        url = Url.parse("https://example.com/api?format=json&limit=10")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.port is None
        assert url.path == "/api"
        assert url.query == "format=json&limit=10"
        assert url.fragment is None

    def test_https_with_fragment(self):
        """Test HTTPS URL with fragment."""
        url = Url.parse("https://docs.example.com/guide#installation")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "docs.example.com"
        assert url.port is None
        assert url.path == "/guide"
        assert url.query is None
        assert url.fragment == "installation"

    def test_https_complete_url(self):
        """Test HTTPS URL with all components."""
        url = Url.parse(
            "https://api.example.com:443/v2/resource?id=123&type=json#details"
        )
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "api.example.com"
        assert url.port == 443
        assert url.path == "/v2/resource"
        assert url.query == "id=123&type=json"
        assert url.fragment == "details"

    def test_https_with_subdomain(self):
        """Test HTTPS URL with subdomain."""
        url = Url.parse("https://www.sub.example.com/page")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "www.sub.example.com"
        assert url.path == "/page"

    def test_https_with_complex_query(self):
        """Test HTTPS URL with complex query string."""
        url = Url.parse(
            "https://example.com/search?q=hello+world&lang=en&page=1&limit=20"
        )
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.path == "/search"
        assert url.query == "q=hello+world&lang=en&page=1&limit=20"

    def test_https_with_standard_port(self):
        """Test HTTPS URL with standard port 443."""
        url = Url.parse("https://example.com:443/")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.port == 443


class TestFileURLParsing:
    """Test File URL parsing."""

    def test_file_basic(self):
        """Test basic file URL parsing."""
        url = Url.parse("file://localhost/")
        assert url.scheme == "file"
        assert url.username is None
        assert url.password is None
        assert url.host == "localhost"
        assert url.port is None
        assert url.path == "/"
        assert url.query is None
        assert url.fragment is None

    def test_file_empty_host(self):
        """Test file URL with empty host (triple slash)."""
        url = Url.parse("file:///path/to/file")
        assert url.scheme == "file"
        assert url.username is None
        assert url.password is None
        assert url.host is None
        assert url.port is None
        assert url.path == "/path/to/file"
        assert url.query is None
        assert url.fragment is None

    def test_file_with_path(self):
        """Test file URL with path."""
        url = Url.parse("file://localhost/path/to/file.html")
        assert url.scheme == "file"
        assert url.username is None
        assert url.password is None
        assert url.host == "localhost"
        assert url.port is None
        assert url.path == "/path/to/file.html"
        assert url.query is None
        assert url.fragment is None

    def test_file_absolute_path(self):
        """Test file URL with absolute path."""
        url = Url.parse("file://localhost/usr/share/doc/index.html")
        assert url.scheme == "file"
        assert url.username is None
        assert url.password is None
        assert url.host == "localhost"
        assert url.port is None
        assert url.path == "/usr/share/doc/index.html"
        assert url.query is None
        assert url.fragment is None

    def test_file_with_fragment(self):
        """Test file URL with fragment."""
        url = Url.parse("file://localhost/path/to/document.html#section2")
        assert url.scheme == "file"
        assert url.username is None
        assert url.password is None
        assert url.host == "localhost"
        assert url.port is None
        assert url.path == "/path/to/document.html"
        assert url.query is None
        assert url.fragment == "section2"

    def test_file_empty_host_with_fragment(self):
        """Test file URL with empty host and fragment."""
        url = Url.parse("file:///usr/share/doc/index.html#intro")
        assert url.scheme == "file"
        assert url.username is None
        assert url.password is None
        assert url.host is None
        assert url.port is None
        assert url.path == "/usr/share/doc/index.html"
        assert url.query is None
        assert url.fragment == "intro"


class TestRFC3986Features:
    """Test RFC 3986 specific features."""

    def test_ipv6_address(self):
        """Test URL with IPv6 address."""
        url = Url.parse("http://[2001:db8::1]/path")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "[2001:db8::1]"
        assert url.port is None
        assert url.path == "/path"

    def test_ipv6_address_with_port(self):
        """Test URL with IPv6 address and port."""
        url = Url.parse("https://[::1]:8080/")
        assert url.scheme == "https"
        assert url.username is None
        assert url.password is None
        assert url.host == "[::1]"
        assert url.port == 8080
        assert url.path == "/"

    def test_ipv4_address(self):
        """Test URL with IPv4 address."""
        url = Url.parse("http://192.168.1.1:8080/path")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "192.168.1.1"
        assert url.port == 8080
        assert url.path == "/path"

    def test_userinfo_username_only(self):
        """Test URL with username in userinfo."""
        url = Url.parse("ftp://user@ftp.example.com/file.txt")
        assert url.scheme == "ftp"
        assert url.username == "user"
        assert url.password is None
        assert url.host == "ftp.example.com"
        assert url.path == "/file.txt"

    def test_userinfo_with_password(self):
        """Test URL with username and password in userinfo."""
        url = Url.parse("ftp://user:pass@ftp.example.com/")
        assert url.scheme == "ftp"
        assert url.username == "user"
        assert url.password == "pass"
        assert url.host == "ftp.example.com"
        assert url.path == "/"

    def test_userinfo_with_empty_password(self):
        """Test URL with username and empty password (colon present)."""
        url = Url.parse("ftp://user:@ftp.example.com/")
        assert url.scheme == "ftp"
        assert url.username == "user"
        assert url.password == ""
        assert url.host == "ftp.example.com"
        assert url.path == "/"

    def test_scheme_with_plus(self):
        """Test URL with scheme containing plus sign."""
        url = Url.parse("git+https://github.com/user/repo")
        assert url.scheme == "git+https"
        assert url.username is None
        assert url.password is None
        assert url.host == "github.com"
        assert url.path == "/user/repo"

    def test_scheme_with_dot(self):
        """Test URL with scheme containing dot."""
        url = Url.parse("custom.scheme://example.com/")
        assert url.scheme == "custom.scheme"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"

    def test_scheme_with_hyphen(self):
        """Test URL with scheme containing hyphen."""
        url = Url.parse("custom-scheme://example.com/")
        assert url.scheme == "custom-scheme"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"

    def test_path_with_special_chars(self):
        """Test URL with special characters in path."""
        url = Url.parse("http://example.com/path/with-dash_underscore~tilde")
        assert url.scheme == "http"
        assert url.username is None
        assert url.password is None
        assert url.host == "example.com"
        assert url.path == "/path/with-dash_underscore~tilde"

    def test_query_with_ampersand(self):
        """Test URL with ampersand in query string."""
        url = Url.parse("http://example.com/?a=1&b=2&c=3")
        assert url.query == "a=1&b=2&c=3"

    def test_query_with_equals(self):
        """Test URL with equals sign in query string."""
        url = Url.parse("http://example.com/?key=value=something")
        assert url.query == "key=value=something"

    def test_fragment_with_slash(self):
        """Test URL with slash in fragment."""
        url = Url.parse("http://example.com/page#section/subsection")
        assert url.fragment == "section/subsection"

    def test_mailto_scheme(self):
        """Test mailto URI scheme (no authority)."""
        url = Url.parse("mailto:user@example.com")
        assert url.scheme == "mailto"
        assert url.username is None
        assert url.password is None
        assert url.host is None
        assert url.port is None
        assert url.path == "user@example.com"
        assert url.query is None
        assert url.fragment is None

    def test_urn_scheme(self):
        """Test URN scheme (no authority)."""
        url = Url.parse("urn:isbn:0-486-27557-4")
        assert url.scheme == "urn"
        assert url.username is None
        assert url.password is None
        assert url.host is None
        assert url.port is None
        assert url.path == "isbn:0-486-27557-4"
        assert url.query is None
        assert url.fragment is None


class TestDataURIScheme:
    """Test data URI scheme."""

    def test_data_simple_text(self):
        """Test simple data URI with text."""
        url = Url.parse("data:text/plain,hello")
        assert url.scheme == "data"
        assert url.username is None
        assert url.password is None
        assert url.host is None
        assert url.port is None
        assert url.path == "text/plain,hello"
        assert url.query is None
        assert url.fragment is None

    def test_data_with_base64(self):
        """Test data URI with base64 encoding."""
        url = Url.parse("data:text/plain;base64,SGVsbG8gV29ybGQh")
        assert url.scheme == "data"
        assert url.host is None
        assert url.path == "text/plain;base64,SGVsbG8gV29ybGQh"

    def test_data_html(self):
        """Test data URI with HTML."""
        url = Url.parse("data:text/html,<h1>Hello</h1>")
        assert url.scheme == "data"
        assert url.host is None
        assert url.path == "text/html,<h1>Hello</h1>"

    def test_data_with_charset(self):
        """Test data URI with charset."""
        url = Url.parse("data:text/plain;charset=utf-8,hello")
        assert url.scheme == "data"
        assert url.host is None
        assert url.path == "text/plain;charset=utf-8,hello"

    def test_data_image(self):
        """Test data URI for image."""
        url = Url.parse("data:image/png;base64,iVBORw0KGgo=")
        assert url.scheme == "data"
        assert url.host is None
        assert url.path == "image/png;base64,iVBORw0KGgo="


class TestURLParsingErrors:
    """Test URL parsing error cases."""

    def test_invalid_url_no_scheme(self):
        """Test that URL without scheme raises ValueError."""
        with pytest.raises(ValueError, match="Invalid URL"):
            Url.parse("example.com/path")

    def test_invalid_url_malformed(self):
        """Test that malformed URL raises ValueError."""
        with pytest.raises(ValueError, match="Invalid URL"):
            Url.parse("not a url at all")

    def test_empty_string(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid URL"):
            Url.parse("")

    def test_scheme_starting_with_digit(self):
        """Test that scheme starting with digit is invalid per RFC 3986."""
        with pytest.raises(ValueError, match="Invalid URL"):
            Url.parse("123abc://example.com/")


class TestDataURLParsing:
    """Test DataURL parsing from path strings."""

    def test_minimal_data_uri(self):
        """Test minimal data URI: data:,"""
        data_url = DataUrl.parse(",")
        assert data_url.mediatype == "text/plain"
        assert data_url.parameters == {"charset": "US-ASCII"}
        assert data_url.is_base64 is False
        assert data_url.data == ""

    def test_empty_path_defaults_to_minimal(self):
        """Test empty path defaults to minimal data URI."""
        data_url = DataUrl.parse("")
        assert data_url.mediatype == "text/plain"
        assert data_url.parameters == {"charset": "US-ASCII"}
        assert data_url.is_base64 is False
        assert data_url.data == ""

    def test_simple_text(self):
        """Test simple text data URI."""
        data_url = DataUrl.parse("text/plain,hello")
        assert data_url.mediatype == "text/plain"
        assert data_url.parameters == {"charset": "US-ASCII"}
        assert data_url.is_base64 is False
        assert data_url.data == "hello"

    def test_text_with_charset(self):
        """Test data URI with charset parameter."""
        data_url = DataUrl.parse("text/plain;charset=UTF-8,Hello World")
        assert data_url.mediatype == "text/plain"
        assert data_url.parameters == {"charset": "UTF-8"}
        assert data_url.is_base64 is False
        assert data_url.data == "Hello World"

    def test_base64_encoded(self):
        """Test base64 encoded data URI."""
        data_url = DataUrl.parse("image/png;base64,iVBORw0KGgo=")
        assert data_url.mediatype == "image/png"
        assert data_url.parameters == {}
        assert data_url.is_base64 is True
        assert data_url.data == "iVBORw0KGgo="

    def test_base64_only_with_default_mediatype(self):
        """Test base64 with default mediatype."""
        data_url = DataUrl.parse(";base64,R0lGODdh")
        assert data_url.mediatype == "text/plain"
        assert data_url.parameters == {"charset": "US-ASCII"}
        assert data_url.is_base64 is True
        assert data_url.data == "R0lGODdh"

    def test_html_content(self):
        """Test HTML content in data URI."""
        data_url = DataUrl.parse("text/html,<h1>Hello</h1>")
        assert data_url.mediatype == "text/html"
        assert data_url.parameters == {}
        assert data_url.is_base64 is False
        assert data_url.data == "<h1>Hello</h1>"

    def test_svg_with_utf8(self):
        """Test SVG with utf8 encoding."""
        data_url = DataUrl.parse(
            "image/svg+xml;charset=utf-8,<svg width='10' height='10'></svg>"
        )
        assert data_url.mediatype == "image/svg+xml"
        assert data_url.parameters == {"charset": "utf-8"}
        assert data_url.is_base64 is False
        assert data_url.data == "<svg width='10' height='10'></svg>"

    def test_multiple_parameters(self):
        """Test data URI with multiple parameters."""
        data_url = DataUrl.parse(
            "text/plain;charset=UTF-8;page=21,the%20data:1234,5678"
        )
        assert data_url.mediatype == "text/plain"
        assert data_url.parameters == {"charset": "UTF-8", "page": "21"}
        assert data_url.is_base64 is False
        assert data_url.data == "the%20data:1234,5678"

    def test_mediatype_with_vendor_prefix(self):
        """Test mediatype with vendor prefix."""
        data_url = DataUrl.parse("text/vnd-example+xyz;foo=bar;base64,R0lGODdh")
        assert data_url.mediatype == "text/vnd-example+xyz"
        assert data_url.parameters == {"foo": "bar"}
        assert data_url.is_base64 is True
        assert data_url.data == "R0lGODdh"

    def test_jpeg_image(self):
        """Test JPEG image data URI."""
        data_url = DataUrl.parse("image/jpeg;base64,/9j/4AAQSkZJRg==")
        assert data_url.mediatype == "image/jpeg"
        assert data_url.parameters == {}
        assert data_url.is_base64 is True
        assert data_url.data == "/9j/4AAQSkZJRg=="

    def test_data_with_special_characters(self):
        """Test data containing special characters."""
        data_url = DataUrl.parse("text/plain,Hello:World;Test=Value")
        assert data_url.mediatype == "text/plain"
        assert data_url.is_base64 is False
        assert data_url.data == "Hello:World;Test=Value"

    def test_missing_comma_raises_error(self):
        """Test that missing comma separator raises ValueError."""
        with pytest.raises(ValueError, match="missing comma separator"):
            DataUrl.parse("text/plain")

    def test_case_insensitive_base64(self):
        """Test that 'base64' is case-insensitive."""
        data_url = DataUrl.parse("text/plain;BASE64,SGVsbG8=")
        assert data_url.is_base64 is True
        assert data_url.data == "SGVsbG8="
