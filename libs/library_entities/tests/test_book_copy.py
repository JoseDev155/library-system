import pytest

from library_entities import (
    BookCopy,
    BusinessRuleError,
    Circulation,
    CopyStatus,
)


def make_copy(**overrides):
    data = {"id": None, "book_id": 1, "inventory_code": "INV-0001"}
    data.update(overrides)
    return BookCopy(**data)


def test_defaults():
    copy = make_copy()
    assert copy.status is CopyStatus.AVAILABLE
    assert copy.circulation is Circulation.LOANABLE


def test_strings_are_converted_to_enums():
    copy = make_copy(status="UNDER_REPAIR", circulation="REFERENCE_ONLY")
    assert copy.status is CopyStatus.UNDER_REPAIR
    assert copy.circulation is Circulation.REFERENCE_ONLY


def test_loan_and_return_cycle():
    copy = make_copy()
    assert copy.can_be_loaned()
    copy.mark_loaned()
    assert copy.status is CopyStatus.LOANED
    assert not copy.can_be_loaned()
    copy.mark_returned()
    assert copy.status is CopyStatus.AVAILABLE


def test_loaned_copy_cannot_be_loaned_again():
    copy = make_copy()
    copy.mark_loaned()
    with pytest.raises(BusinessRuleError):
        copy.mark_loaned()


def test_reference_only_copy_cannot_be_loaned():
    copy = make_copy(circulation=Circulation.REFERENCE_ONLY)
    assert not copy.can_be_loaned()
    with pytest.raises(BusinessRuleError):
        copy.mark_loaned()


def test_reserved_copy_can_be_loaned():
    copy = make_copy()
    copy.mark_reserved()
    assert copy.can_be_loaned()
    copy.mark_loaned()
    assert copy.status is CopyStatus.LOANED


def test_return_requires_loaned_copy():
    with pytest.raises(BusinessRuleError):
        make_copy().mark_returned()


def test_reserve_and_release():
    copy = make_copy()
    copy.mark_reserved()
    assert copy.status is CopyStatus.RESERVED
    copy.release_reservation()
    assert copy.status is CopyStatus.AVAILABLE


def test_only_available_copy_can_be_reserved():
    copy = make_copy()
    copy.mark_loaned()
    with pytest.raises(BusinessRuleError):
        copy.mark_reserved()


def test_release_requires_reserved_copy():
    with pytest.raises(BusinessRuleError):
        make_copy().release_reservation()


def test_repair_cycle():
    copy = make_copy()
    copy.send_to_repair()
    assert copy.status is CopyStatus.UNDER_REPAIR
    assert not copy.can_be_loaned()
    copy.finish_repair()
    assert copy.status is CopyStatus.AVAILABLE


def test_repair_transitions_are_guarded():
    copy = make_copy()
    with pytest.raises(BusinessRuleError):
        copy.finish_repair()
    copy.mark_loaned()
    with pytest.raises(BusinessRuleError):
        copy.send_to_repair()


def test_withdraw():
    copy = make_copy()
    copy.withdraw()
    assert copy.status is CopyStatus.WITHDRAWN
    assert not copy.can_be_loaned()


def test_loaned_copy_cannot_be_withdrawn():
    copy = make_copy()
    copy.mark_loaned()
    with pytest.raises(BusinessRuleError):
        copy.withdraw()
