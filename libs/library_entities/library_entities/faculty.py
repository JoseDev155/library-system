import re
from dataclasses import dataclass

_CODE_PATTERN = re.compile(r"^[0-9]{3}$")


@dataclass(frozen=True, slots=True)
class Faculty:
    """Faculty or administrative unit (spec, section 8.3)."""

    code: str
    name: str

    def __post_init__(self) -> None:
        if not _CODE_PATTERN.match(self.code):
            raise ValueError("Faculty code must have exactly 3 digits")
