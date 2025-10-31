# TODO
from dataclasses import dataclass


@dataclass(frozen=True)
class NoCache: ...


@dataclass(frozen=True)
class NoStore: ...


@dataclass(frozen=True)
class NoTransform: ...


@dataclass(frozen=True)
class OnlyIfCached: ...


@dataclass(frozen=True)
class MaxAge:
    delta_seconds: int


@dataclass(frozen=True)
class MaxStale:
    delta_seconds: int


@dataclass(frozen=True)
class MinFresh:
    delta_seconds: int


@dataclass(frozen=True)
class Public: ...


@dataclass(frozen=True)
class UnknownToken:
    name: str
    value: str | None


RequestCacheControlToken = (
    NoCache
    | NoStore
    | NoTransform
    | OnlyIfCached
    | MaxAge
    | MaxStale
    | MinFresh
    | Public
    | UnknownToken
)


def parse_request_cache_control(s: str) -> list[RequestCacheControlToken]:
    """
    Expect to receive a valid Cache-Control header value.
    For instance, when there is "Cache-Control: max-age=3600\r\n" header, the "s" parameter should be "max-age=3600"
    """
    ...
