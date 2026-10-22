class Book:
    """Catalog title. Physical items are BookCopy objects."""

    def __init__(
        self,
        id: int | None,
        title: str,
        authors: list[str],
        category: str,
        faculty_code: str,
        call_number: str,
        isbn: str | None = None,
        publisher: str | None = None,
        edition: str | None = None,
        year: int | None = None,
    ) -> None:
        if not title.strip():
            raise ValueError("Book title cannot be empty")
        if not authors:
            raise ValueError("Book needs at least one author")
        self.id = id
        self.isbn = isbn or None
        self.title = title
        self.authors = list(authors)
        self.category = category
        self.faculty_code = faculty_code
        self.publisher = publisher
        self.edition = edition
        self.year = year
        self.call_number = call_number

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r})"
