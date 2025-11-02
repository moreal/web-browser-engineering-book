import dataclasses
import re
import os.path
from dataclasses import dataclass
from typing import cast, override

from browser.cache import HttpCache
from browser.protocols.http.media_type import InvalidMediaType
from browser.singleton import GlobalMemoryCache
from browser.content import (
    Content,
    UnknownContent,
    recognize_content,
)
from browser.handler import RedirectInfo, UrlHandler
from browser.protocols.http.headers.cache_control.response import (
    parse_response_cache_control,
)

from browser.protocols.http.headers.cache_control import response as cache_control_token
from browser.protocols.http.request import HttpRequest
from browser.protocols.http.response import HttpResponse
from browser.connection import request_http
from browser.url import HttpFamilyUrl, Url

import time

__all__ = (
    "HttpHandler",
    "recognize_response",
)


def get_current_epoch():
    return int(time.time())


HTTP_KEEP_ALIVE_FLAG: bool = True


@dataclass(frozen=True)
class HttpHandler(UrlHandler):
    cache: HttpCache = GlobalMemoryCache

    @override
    def fetch(self, url: Url):
        http_family_url = HttpFamilyUrl.from_url(url)
        request = HttpRequest(
            method="GET",
            path=url.path or "/",
            headers={
                "Host": http_family_url.host,
                "Connection": "keep-alive" if HTTP_KEEP_ALIVE_FLAG else "close",
                "Accept-Encoding": "gzip",
            },
            version="1.1",
        )
        response = request_http(http_family_url, request)
        if (cache_control := response.headers.get("cache-control")) is not None:
            response_cache_control_tokens = parse_response_cache_control(cache_control)
            max_age_token = cast(
                cache_control_token.MaxAge | None,
                next(
                    filter(
                        lambda x: isinstance(x, cache_control_token.MaxAge),
                        response_cache_control_tokens,
                    ),
                    None,
                ),
            )
            max_age = get_current_epoch() + (
                max_age_token.delta_seconds if max_age_token is not None else 5
            )
            if not any(
                map(
                    lambda x: isinstance(x, cache_control_token.NoStore),
                    response_cache_control_tokens,
                )
            ):
                self.cache.set(http_family_url, response, max_age)

        if (
            300 <= response.status_code < 400
            and (location_header_value := response.headers.get("location")) is not None
        ):
            if re.match(r"^[^:/]+://", location_header_value):
                redirect_url = Url.parse(location_header_value)
                return RedirectInfo(url=redirect_url)
            else:
                # FIXME: resolve relative path via URL.resolve
                next_path = os.path.join(
                    http_family_url.path or "/", location_header_value
                )
                redirect_url = dataclasses.replace(http_family_url, path=next_path)
                return RedirectInfo(url=redirect_url.to_url())
        return recognize_response(response)


def recognize_response(response: HttpResponse) -> Content:
    content_type = response.headers.content_type()
    if content_type is None or isinstance(content_type, InvalidMediaType):
        return UnknownContent(media_type=None, bytes=response.body)

    return recognize_content(content_type, response.body)
