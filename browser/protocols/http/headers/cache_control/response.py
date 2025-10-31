from dataclasses import dataclass


@dataclass(frozen=True)
class NoCache:
    header_names: list[str]


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
class MustRevalidate: ...


@dataclass(frozen=True)
class UnknownToken:
    name: str
    value: str | None


ResponseCacheControlToken = (
    NoCache
    | NoStore
    | NoTransform
    | OnlyIfCached
    | MaxAge
    | MaxStale
    | MinFresh
    | MustRevalidate
    | UnknownToken
)


def parse_response_cache_control(s: str) -> list[ResponseCacheControlToken]:
    """
    Expect to receive a valid Cache-Control header value.
    For instance, when there is "Cache-Control: max-age=3600\r\n" header, the "s" parameter should be "max-age=3600"
    """
    result: list[ResponseCacheControlToken] = []
    for token in map(str.strip, s.split(",")):
        split = token.split("=")
        name = split[0]
        value = split[1] if len(split) > 1 else None

        # Rewrite with match-case
        match (name, value):
            case ("no-cache", None):
                result.append(NoCache(header_names=[]))
            case ("no-cache", str()):
                result.append(
                    NoCache(header_names=[name.strip() for name in value.split(",")])
                )
            case ("no-store", None):
                result.append(NoStore())
            case ("no-transform", None):
                result.append(NoTransform())
            case ("only-if-cached", _):
                result.append(OnlyIfCached())
            case ("max-age", str()):
                result.append(MaxAge(delta_seconds=int(value)))
            case ("max-stale", str()):
                result.append(MaxStale(delta_seconds=int(value)))
            case ("min-fresh", str()):
                result.append(MinFresh(delta_seconds=int(value)))
            case ("must-revalidate", None):
                result.append(MustRevalidate())
            case _:
                result.append(UnknownToken(name=token, value=value))

    return result
