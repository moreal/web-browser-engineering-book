from typing import override
from browser.content import recognize_content
from browser.handler import UrlHandler
from browser.url import DataUrl


__all__ = ("DataUrlHandler",)


class DataUrlHandler(UrlHandler[DataUrl]):
    @override
    def fetch(self, url: DataUrl):
        data = url.get_data()
        if isinstance(data, str):
            data = (
                data.encode(charset)
                if (charset := url.parameters.get("charset")) is not None
                else data.encode()
            )

        return recognize_content(url.mediatype, data)
