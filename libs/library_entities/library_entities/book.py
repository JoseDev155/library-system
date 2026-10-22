from dataclasses import dataclass


# EN: Catalog title. Physical items are BookCopy objects.
# ES: Título del catálogo. Los ejemplares físicos son BookCopy.
@dataclass(slots=True)
class Book:
    id: int | None
    title: str
    authors: list[str]
    category: str
    faculty_code: str
    call_number: str
    isbn: str | None = None
    publisher: str | None = None
    edition: str | None = None
    year: int | None = None

    def __post_init__(self) -> None:
        # EN: An empty ISBN means "no ISBN", so it stays unique when present.
        # ES: Un ISBN vacío significa "sin ISBN", así sigue siendo único si existe.
        self.isbn = self.isbn or None
