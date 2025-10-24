from dataclasses import dataclass
from typing import Final, Literal

__all__ = (
    "HttpRequest",
    "HTTP_LINE_SEPARATOR",
)


HTTP_LINE_SEPARATOR = "\r\n"


@dataclass(frozen=True)
class HttpRequest:
    method: str
    path: str
    headers: dict[str, str]
    version: Literal["1.0", "1.1"] = "1.0"


class HttpRequestEncoder:
    def __init__(self, user_agent: str = "LocalBrowser/0.0"):
        self.user_agent: Final[str] = user_agent

    def encode(self, request: HttpRequest) -> bytes:
        headers = request.headers.copy()

        if request.version == "1.1":
            if "Connection" not in headers:
                headers["Connection"] = "close"

        head = f"{request.method} {request.path} HTTP/{request.version}\r\n"
        body = "".join(
            f"{name}: {value}{HTTP_LINE_SEPARATOR}" for name, value in headers.items()
        )

        return (head + body + HTTP_LINE_SEPARATOR).encode("utf8")
