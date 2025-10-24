from dataclasses import dataclass
from browser.protocols.http.request import HttpRequest


__all__ = ("HttpResponse",)


@dataclass(frozen=True)
class HttpResponse:
    version: str
    status_code: int
    status_message: str
    headers: dict[str, str]
    body: str

    request: HttpRequest
