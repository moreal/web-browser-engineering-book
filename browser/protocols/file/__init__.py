from dataclasses import dataclass


@dataclass(frozen=True)
class FileRequest:
    path: str
