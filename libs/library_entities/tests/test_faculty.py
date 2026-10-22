import pytest

from library_entities import Faculty


def test_valid_faculty():
    faculty = Faculty("101", "Ingeniería y Tecnología")
    assert faculty.code == "101"


@pytest.mark.parametrize("code", ["10", "1011", "ABC", "", "10a"])
def test_invalid_code_is_rejected(code):
    with pytest.raises(ValueError):
        Faculty(code, "Any")


def test_faculty_is_immutable():
    faculty = Faculty("101", "Ingeniería y Tecnología")
    with pytest.raises(AttributeError):
        faculty.code = "102"
