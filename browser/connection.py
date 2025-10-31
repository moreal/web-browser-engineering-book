import socket
import ssl
from typing import Literal
from browser.protocols.http.request import (
    HTTP_LINE_SEPARATOR,
    HttpRequest,
    HttpRequestEncoder,
)
from browser.protocols.http.response import HttpResponse


__all__ = ("Connection",)

HTTP_FAMILY_SCHEME = Literal["http", "https"]

DEFAULT_PORT: dict[HTTP_FAMILY_SCHEME, int] = {
    "http": 80,
    "https": 443,
}


def get_default_port(scheme: HTTP_FAMILY_SCHEME) -> int:
    return DEFAULT_PORT[scheme]


class Connection:
    """HTTP connection"""

    def __init__(
        self, scheme: Literal["http", "https"], host: str, port: int | None = None
    ) -> None:
        self.scheme: Literal["http", "https"] = scheme
        self.host: str = host
        self.port: int = port or DEFAULT_PORT[scheme]

    def _create_socket(self):
        _socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )

        if self.scheme == "https":
            context = ssl.create_default_context()
            _socket = context.wrap_socket(_socket, server_hostname=self.host)

        return _socket

    def request(
        self,
        request: HttpRequest,
        encoder: HttpRequestEncoder | None = None,
    ) -> HttpResponse:
        encoder = encoder or HttpRequestEncoder()

        with self._create_socket() as s:
            s.connect((self.host, self.port))
            _sent_bytes = s.send(encoder.encode(request))

            response = s.makefile("rb", newline=HTTP_LINE_SEPARATOR)

            statusline = response.readline().decode("iso-8859-1")
            version, status_code, status_message = statusline.split(" ", 2)

            headers = dict[str, str]()
            while (line := response.readline()) != b"\r\n":
                name, value = line.decode("iso-8859-1").split(":", 1)
                headers[name.strip().casefold()] = value.strip()

            body = response.read()

        return HttpResponse(
            version=version,
            status_code=int(status_code),
            status_message=status_message,
            headers=headers,
            body=body,
            request=request,
        )
