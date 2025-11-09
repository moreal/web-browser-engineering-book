from typing import override

from browser.content import Content, HtmlContent
from browser.handler import RedirectInfo, UrlHandler
from browser.url import AboutUrl, Url


class AboutUrlHandler(UrlHandler):
    @override
    def fetch(self, url: Url) -> Content | RedirectInfo:
        match AboutUrl.from_url(url):
            case AboutUrl(path="blank"):
                return HtmlContent(data=b"<html><body>Blank page</body></html>")
            case _:
                return HtmlContent(data=b"Failed to parse URL with about: scheme")
