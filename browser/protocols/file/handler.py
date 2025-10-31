from typing import override
from browser.content import PlainTextContent
from browser.handler import UrlHandler
from browser.url import Url


class FileUrlHandler(UrlHandler):
    @override
    def fetch(self, url: Url):
        assert url.path is not None
        # FIXME: needs to load binary contents also.
        with open(url.path, "r") as file:
            return PlainTextContent(text=file.read())
