from browser.protocols.handler import Handler
from browser.url import HttpUrl
from browser.content import Content


class HttpHandler(Handler[HttpUrl]):
    def fetch(self, url: HttpUrl) -> Content: ...
