from dataclasses import dataclass
from browser.protocols.http.request import HttpRequest
from browser.protocols.http.header_map import HeaderMap


__all__ = ("HttpResponse",)


@dataclass(frozen=True)
class HttpResponse:
    version: str
    status_code: int
    status_message: str
    headers: HeaderMap
    body: bytes

    request: HttpRequest
