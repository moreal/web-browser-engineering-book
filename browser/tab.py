from browser.url import Url, ConcreteUrl, to_concrete
from browser.protocols import handle_url


class Tab:
    def __init__(self, url: Url, body: str = ""):
        self.url: Url = url
        self._body: str = body

    @staticmethod
    def open(url: Url) -> "Tab":
        concrete_url = to_concrete(url)
        body = handle_url(concrete_url)

        return Tab(url=url, body=body)

    @property
    def body(self) -> str:
        return self._body
