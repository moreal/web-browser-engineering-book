import socket
from browser.protocols.http.request import (
    HTTP_LINE_SEPARATOR,
    HttpRequest,
    HttpRequestEncoder,
)
from browser.protocols.http.response import HttpResponse

__all__ = ("HttpConnection",)


DEFAULT_PORT = 80


class HttpConnection:
    def __init__(self, host: str, port: int | None = None) -> None:
        self.host: str = host
        self.port: int = port or DEFAULT_PORT

    def _create_socket(self):
        return socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP
        )

    def send(
        self,
        request: HttpRequest,
        encoder: HttpRequestEncoder | None = None,
    ) -> HttpResponse:
        encoder = encoder or HttpRequestEncoder()

        with self._create_socket() as s:
            s.connect((self.host, self.port))
            _sent_bytes = s.send(encoder.encode(request))

            response = s.makefile("r", encoding="utf8", newline=HTTP_LINE_SEPARATOR)

            statusline = response.readline()
            version, status_code, status_message = statusline.split(" ", 2)

            headers = dict[str, str]()
            while (line := response.readline()) != "\r\n":
                name, value = line.split(":", 1)
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
