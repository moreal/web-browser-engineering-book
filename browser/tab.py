from browser.url import URL, ConcreteUrl, to_concrete
from browser.protocols import handle_url


class Tab:
    def __init__(self, url: URL, body: str = ""):
        self.url: URL = url
        self._body: str = body

    @staticmethod
    def open(url: URL) -> "Tab":
        concrete_url = to_concrete(url)
        body = handle_url(concrete_url)

        return Tab(url=url, body=body)

    @property
    def body(self) -> str:
        return self._body
