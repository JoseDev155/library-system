from library_entities import Book


def make_book(**overrides):
    data = {
        "id": None,
        "title": "Clean Code",
        "authors": ["Robert C. Martin"],
        "category": "Software",
        "faculty_code": "101",
        "call_number": "005.1 MAR",
    }
    data.update(overrides)
    return Book(**data)


def test_book_keeps_isbn_when_present():
    assert make_book(isbn="9780132350884").isbn == "9780132350884"


def test_empty_isbn_becomes_none():
    assert make_book(isbn="").isbn is None


def test_missing_isbn_is_none():
    assert make_book().isbn is None
