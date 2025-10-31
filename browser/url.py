import base64
from dataclasses import dataclass
import re
from typing import Literal

__all__ = ("Url", "DataUrl")

QueryValueType = str | list[str]


@dataclass(frozen=True)
class Url:
    scheme: str
    username: str | None
    password: str | None
    host: str | None
    port: int | None
    path: str | None
    # FIXME: it doens't parse query string (e.g., "key[]=a&key[3]=b")
    query: str | None
    fragment: str | None

    @staticmethod
    def parse(s: str) -> "Url":
        # RFC 3986 compliant URL regex pattern
        # URI = scheme ":" ["//" authority] path ["?" query] ["#" fragment]
        # authority = [userinfo "@"] host [":" port]

        # Scheme: starts with letter, followed by letters, digits, +, -, or .
        scheme = r"(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)"

        # Userinfo (optional): username[:password]@
        # Unreserved: A-Z a-z 0-9 - . _ ~
        # Sub-delims: ! $ & ' ( ) * + , ; =
        # Also allows : and percent-encoded chars
        userinfo = r"(?:(?P<username>[a-zA-Z0-9\-._~!$&'()*+,;=%]+)(?::(?P<password>[a-zA-Z0-9\-._~!$&'()*+,;=%]*))?@)?"

        # Host can be:
        # - IPv6: enclosed in brackets [...]
        # - IPv4: dot-decimal notation
        # - Registered name: letters, digits, hyphens, dots, underscores, tildes
        ipv6 = r"\[[0-9a-fA-F:]+\]"
        ipv4 = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        registered_name = r"[a-zA-Z0-9\-._~!$&'()*+,;=%]*"
        host = rf"(?P<hostname>{ipv6}|{ipv4}|{registered_name})"

        # Port (optional): decimal digits
        port = r"(?::(?P<port>\d+))?"

        # Authority (optional): [userinfo "@"] host [":" port]
        authority = rf"(?://(?:{userinfo}{host}{port}))?"

        # Path: sequence of segments separated by /
        # Can contain unreserved chars, percent-encoded, sub-delims, :, @
        # For URIs without authority, path can contain additional characters
        # Matches everything except ? and # (which start query and fragment)
        path = r"(?P<path>[^?#]*)"

        # Query (optional): after ?, can contain any character except #
        query = r"(?:\?(?P<query>[^#]*))?"

        # Fragment (optional): after #, can contain any remaining characters
        fragment = r"(?:#(?P<fragment>.*))?"

        # Complete regex pattern
        regex = rf"^{scheme}:{authority}{path}{query}{fragment}$"

        match = re.match(regex, s)
        if not match:
            raise ValueError("Invalid URL")

        scheme_value = match.group("scheme")
        username_value = match.group("username")
        password_value = match.group("password")
        hostname = match.group("hostname") or None
        port_value = int(match.group("port")) if match.group("port") else None
        path_value = match.group("path") or None
        query_value = match.group("query")
        fragment_value = match.group("fragment")

        return Url(
            scheme=scheme_value,
            username=username_value,
            password=password_value,
            host=hostname,
            port=port_value,
            path=path_value,
            query=query_value,
            fragment=fragment_value,
        )

    def resolve(self, relative_url: str) -> Url:
        return self


@dataclass(frozen=True)
class HttpFamilyUrl:
    scheme: Literal["http", "https"]
    username: str | None
    password: str | None
    host: str
    port: int | None
    path: str | None
    query: str | None
    fragment: str | None

    def to_url(self) -> Url:
        return Url(
            scheme=self.scheme,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )


@dataclass(frozen=True)
class FileUrl:
    host: str
    path: str | None


@dataclass(frozen=True)
class DataUrl:
    """
    Data URI scheme parser according to RFC 2397.

    Syntax: data:[<mediatype>][;base64],<data>

    - mediatype: optional MIME type with optional parameters (e.g., text/plain;charset=UTF-8)
                 defaults to text/plain;charset=US-ASCII
    - base64: optional indicator that data is base64-encoded
    - data: the actual data (may be empty)
    """

    mediatype: str  # e.g., "text/plain", "image/png"
    parameters: dict[str, str]  # e.g., {"charset": "UTF-8"}
    is_base64: bool
    data: str

    @staticmethod
    def parse(path: str) -> "DataUrl":
        """
        Parse a data URI path (without the 'data:' scheme prefix).

        Examples:
            - "" -> mediatype=text/plain, charset=US-ASCII, data=""
            - "text/html,<h1>Hello</h1>" -> mediatype=text/html, data="<h1>Hello</h1>"
            - "text/plain;charset=UTF-8,Hello" -> mediatype=text/plain, charset=UTF-8, data="Hello"
            - "image/png;base64,iVBORw0..." -> mediatype=image/png, base64=True, data="iVBORw0..."
            - ";base64,R0lGODdh" -> mediatype=text/plain, base64=True, data="R0lGODdh"
        """
        if not path:
            # Minimal data URI: "data:,"
            path = ","

        # The comma is required and separates metadata from data
        if "," not in path:
            raise ValueError("Invalid data URI: missing comma separator")

        metadata, data = path.split(",", 1)

        # Parse metadata part: [<mediatype>][;<param>=<value>]*[;base64]
        parts = metadata.split(";") if metadata else []

        # First part is the mediatype (if present and not a parameter)
        mediatype = "text/plain"
        parameters: dict[str, str] = {}
        is_base64 = False

        for i, part in enumerate(parts):
            part = part.strip()
            if not part:
                continue

            # Check if it's "base64" indicator
            if part.lower() == "base64":
                is_base64 = True
            # Check if it's a parameter (contains '=')
            elif "=" in part:
                key, value = part.split("=", 1)
                parameters[key.strip()] = value.strip()
            # First non-parameter, non-base64 part is the mediatype
            elif i == 0:
                mediatype = part
            else:
                # If we encounter a part without '=' that's not first and not 'base64',
                # it might be a malformed URI, but we'll treat it as part of mediatype
                pass

        # Set default charset if not specified and mediatype is text/plain
        if mediatype == "text/plain" and "charset" not in parameters:
            parameters["charset"] = "US-ASCII"

        return DataUrl(
            mediatype=mediatype,
            parameters=parameters,
            is_base64=is_base64,
            data=data,
        )

    def get_data(self) -> str | bytes:
        if self.is_base64:
            data = base64.b64decode(self.data)

            if self.mediatype.startswith("text/"):
                charset = self.parameters["charset"]
                data = data.decode(charset)

            return data
        else:
            return self.data


ConcreteUrl = FileUrl | DataUrl | HttpFamilyUrl


def to_concrete(url: Url) -> ConcreteUrl:
    match url.scheme:
        case "data":
            return DataUrl.parse(url.path or "")
        case "http" | "https":
            if url.host is None:
                raise ValueError("'host' is required for HTTP URLs")
            return HttpFamilyUrl(
                scheme=url.scheme,
                username=url.username,
                password=url.password,
                host=url.host,
                port=url.port,
                path=url.path,
                query=url.query,
                fragment=url.fragment,
            )
        case "file":
            return FileUrl(
                host=url.host or "localhost",
                path=url.path,
            )
        case _:
            raise ValueError(f"Unsupported scheme: {url.scheme}")
