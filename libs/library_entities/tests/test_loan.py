from datetime import UTC, date, datetime, timedelta

import pytest

from library_entities import BusinessRuleError, Loan, LoanStatus

LOANED_AT = datetime(2024, 3, 1, 10, 0, tzinfo=UTC)


def make_loan(**overrides):
    data = {
        "id": None,
        "copy_id": 1,
        "user_id": "2024-PM-101-01",
        "loaned_by": "2020-GL-900-01",
        "loaned_at": LOANED_AT,
        "due_at": LOANED_AT + timedelta(days=7),
    }
    data.update(overrides)
    return Loan(**data)


def test_new_loan_is_active():
    loan = make_loan()
    assert loan.is_active()
    assert loan.renewals == 0


def test_due_date_must_be_after_loan_date():
    with pytest.raises(ValueError):
        make_loan(due_at=LOANED_AT)


def test_status_string_is_converted():
    assert make_loan(status="RETURNED").status is LoanStatus.RETURNED


def test_is_overdue_depends_on_due_date():
    loan = make_loan()
    assert not loan.is_overdue(LOANED_AT + timedelta(days=7))
    assert loan.is_overdue(LOANED_AT + timedelta(days=7, seconds=1))


def test_returned_loan_is_never_overdue():
    loan = make_loan()
    loan.close(LOANED_AT + timedelta(days=3))
    assert not loan.is_overdue(LOANED_AT + timedelta(days=30))


def test_renew_extends_due_date():
    loan = make_loan()
    loan.renew(max_renewals=1, loan_days=7)
    assert loan.due_at == LOANED_AT + timedelta(days=14)
    assert loan.renewals == 1


def test_renew_respects_maximum():
    loan = make_loan()
    loan.renew(max_renewals=1, loan_days=7)
    with pytest.raises(BusinessRuleError):
        loan.renew(max_renewals=1, loan_days=7)


def test_returned_loan_cannot_be_renewed():
    loan = make_loan()
    loan.close(LOANED_AT + timedelta(days=1))
    with pytest.raises(BusinessRuleError):
        loan.renew(max_renewals=2, loan_days=7)


def test_days_late_for_open_loan():
    loan = make_loan()
    assert loan.days_late(date(2024, 3, 8)) == 0
    assert loan.days_late(date(2024, 3, 12)) == 4


def test_days_late_uses_return_date_once_closed():
    loan = make_loan()
    loan.close(datetime(2024, 3, 10, 9, 0, tzinfo=UTC))
    assert loan.days_late(date(2024, 4, 1)) == 2


def test_close_sets_status_and_date():
    loan = make_loan()
    returned_at = LOANED_AT + timedelta(days=2)
    loan.close(returned_at)
    assert loan.status is LoanStatus.RETURNED
    assert loan.returned_at == returned_at


def test_cannot_close_twice():
    loan = make_loan()
    loan.close(LOANED_AT + timedelta(days=2))
    with pytest.raises(BusinessRuleError):
        loan.close(LOANED_AT + timedelta(days=3))
