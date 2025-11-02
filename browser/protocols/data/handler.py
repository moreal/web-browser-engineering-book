from typing import override
from browser.content import recognize_content
from browser.handler import UrlHandler
from browser.url import Url, DataUrlData


__all__ = ("DataUrlHandler",)


class DataUrlHandler(UrlHandler):
    @override
    def fetch(self, url: Url):
        if url.path is None:
            raise ValueError("Invalid URL. data: scheme needs path")
        data_url = DataUrlData.parse(url.path)
        data = data_url.get_data()
        if isinstance(data, str):
            data = (
                data.encode(charset)
                if (charset := data_url.media_type.parameters.get("charset"))
                is not None
                else data.encode()
            )

        return recognize_content(data_url.media_type, data)
