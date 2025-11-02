from collections.abc import Iterable, Iterator, Mapping
from typing import override

from browser.protocols.http.media_type import (
    InvalidMediaType,
    MediaType,
    parse_media_type,
)


class HeaderMap(Mapping[str, str]):
    _headers: dict[str, str]

    def __init__(
        self, headers: Mapping[str, str] | Iterable[tuple[str, str]] | None = None
    ):
        self._headers = (
            {}
            if headers is None
            else {
                key.casefold(): value
                for key, value in (
                    headers.items() if isinstance(headers, Mapping) else headers
                )
            }
        )

    @override
    def __getitem__(self, key: str) -> str:
        return self._headers[key]

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._headers)

    @override
    def __len__(self) -> int:
        return len(self._headers)

    def content_type(self) -> MediaType | InvalidMediaType | None:
        if (_content_type := self._headers.get("content-type")) is None:
            return None

        return parse_media_type(_content_type)
