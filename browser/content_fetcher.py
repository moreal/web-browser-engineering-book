from browser.handler import RedirectInfo
from browser.url import Url
from browser.content import Content

from browser.handler import UrlHandler
from browser.protocols.data.handler import DataUrlHandler
from browser.protocols.file.handler import FileUrlHandler
from browser.protocols.view_source import ViewSourceUrlHandler
from browser.protocols.http.handler import HttpHandler

# Lazy initialization to avoid circular imports
_handlers: dict[str, UrlHandler] | None = None


def _initialize_handlers() -> dict[str, UrlHandler]:
    """Initialize handlers on first use to avoid circular import issues."""
    return {
        "http": HttpHandler(),
        "https": HttpHandler(),
        "file": FileUrlHandler(),
        "data": DataUrlHandler(),
        "view-source": ViewSourceUrlHandler(fetch_content),
    }


def get_handler(scheme: str) -> UrlHandler | None:
    global _handlers
    if _handlers is None:
        _handlers = _initialize_handlers()

    handler = _handlers.get(scheme)
    if handler is None:
        raise ValueError(f"Unsupported scheme: {scheme}")
    return handler


def fetch_content(url: Url) -> Content:
    return _fetch_content(url)


def _fetch_content(url: Url, max_redirects: int = 20) -> Content:
    if max_redirects <= 0:
        raise ValueError("Max redirects exceeded")

    result = None
    while True:
        if (handler := get_handler(url.scheme)) is None:
            raise ValueError(f"Cannot handle {url}")

        result = handler.fetch(url)
        match result:
            case RedirectInfo():
                return _fetch_content(result.url, max_redirects - 1)
            case _:
                return result
