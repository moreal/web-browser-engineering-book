from browser.handler import UrlHandler
from browser.protocols.data.handler import DataUrlHandler
from browser.protocols.file.handler import FileUrlHandler
from browser.protocols.view_source import ViewSourceUrlHandler
from browser.protocols.http.handler import HttpHandler
from browser.singleton import GlobalContentFetcher

SCHEME_TO_HANDLER = {
    "http": HttpHandler(),
    "https": HttpHandler(),
    "file": FileUrlHandler(),
    "data": DataUrlHandler(),
    "view-source": ViewSourceUrlHandler(GlobalContentFetcher),
}


def get_handler(scheme: str) -> UrlHandler | None:
    handler = SCHEME_TO_HANDLER.get(scheme)
    if handler is None:
        raise ValueError(f"Unsupported scheme: {scheme}")
    return handler
