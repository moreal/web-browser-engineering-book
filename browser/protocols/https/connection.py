import ssl
from typing import override

from browser.protocols.http.connection import HttpConnection

__all__ = ("HttpsConnection",)


DEFAULT_PORT = 443


class HttpsConnection(HttpConnection):
    def __init__(self, host: str, port: int | None = None) -> None:
        super().__init__(host, port or DEFAULT_PORT)

    @override
    def _create_socket(self):
        context = ssl.create_default_context()
        return context.wrap_socket(super()._create_socket(), server_hostname=self.host)
