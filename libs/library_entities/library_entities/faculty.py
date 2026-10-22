import re

_CODE_PATTERN = re.compile(r"^[0-9]{3}$")


class Faculty:
    """Faculty or administrative unit (spec, section 8.3)."""

    def __init__(self, code: str, name: str) -> None:
        if not _CODE_PATTERN.match(code):
            raise ValueError("Faculty code must have exactly 3 digits")
        if not name.strip():
            raise ValueError("Faculty name cannot be empty")
        self.code = code
        self.name = name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Faculty) and self.code == other.code

    def __hash__(self) -> int:
        return hash(self.code)

    def __repr__(self) -> str:
        return f"Faculty(code={self.code!r}, name={self.name!r})"
