from dataclasses import dataclass, field


@dataclass(frozen=True, eq=True)
class MediaType:
    """
    media type implementation used in Content-Type header
    (ref https://httpwg.org/specs/rfc9110.html#rfc.section.8.3)
    """

    type: str
    subtype: str
    parameters: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, eq=True)
class InvalidMediaType:
    raw: str


def parse_media_type(media_type: str) -> MediaType | InvalidMediaType:
    """Parse a media type string into a MediaType object."""

    parts = media_type.split(";")
    match parts:
        case []:
            return InvalidMediaType(raw=media_type)
        case [main_part, *param_parts]:
            match main_part.strip().split("/"):
                case [str() as type, str() as subtype]:
                    type = type.strip().lower()
                    subtype = subtype.strip().lower()
                case _:
                    return InvalidMediaType(raw=media_type)
        case _:
            return InvalidMediaType(raw=media_type)

    parameters = dict(_parse_parameter(param) for param in param_parts)
    return MediaType(type=type, subtype=subtype, parameters=parameters)


def _parse_parameter(param: str) -> tuple[str, str]:
    match param.strip().split("=", 1):
        case [key, value]:
            return key, value
        case _:
            raise ValueError("Invalid parameter format")
