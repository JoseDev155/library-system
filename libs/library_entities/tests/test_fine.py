from decimal import Decimal

import pytest

from library_entities import BusinessRuleError, Fine, FineStatus


def make_fine(**overrides):
    data = {
        "id": None,
        "loan_id": 1,
        "user_id": "2024-PM-101-01",
        "days_late": 3,
        "rate_per_day": Decimal("0.25"),
        "amount": Decimal("0.75"),
    }
    data.update(overrides)
    return Fine(**data)


def test_for_late_loan_computes_amount_and_keeps_rate():
    fine = Fine.for_late_loan(1, "2024-PM-101-01", 4, Decimal("0.25"))
    assert fine.amount == Decimal("1.00")
    assert fine.rate_per_day == Decimal("0.25")
    assert fine.status is FineStatus.PENDING


def test_for_late_loan_rounds_to_cents():
    fine = Fine.for_late_loan(1, "2024-PM-101-01", 3, Decimal("0.335"))
    assert fine.amount == Decimal("1.01")


@pytest.mark.parametrize("days_late", [0, -1])
def test_days_late_must_be_positive(days_late):
    with pytest.raises(ValueError):
        make_fine(days_late=days_late)


def test_negative_amounts_are_rejected():
    with pytest.raises(ValueError):
        make_fine(amount=Decimal(-1))
    with pytest.raises(ValueError):
        make_fine(rate_per_day=Decimal("-0.1"))


def test_status_string_is_converted():
    assert make_fine(status="PAID").status is FineStatus.PAID


def test_pay_pending_fine():
    fine = make_fine()
    assert fine.is_pending()
    fine.pay()
    assert fine.status is FineStatus.PAID
    assert not fine.is_pending()


def test_fine_is_paid_only_once():
    fine = make_fine()
    fine.pay()
    with pytest.raises(BusinessRuleError):
        fine.pay()


def test_waive_records_reason_and_author():
    fine = make_fine()
    fine.waive("Library error", "2020-AD-900-01")
    assert fine.status is FineStatus.WAIVED
    assert fine.waiver_reason == "Library error"
    assert fine.waived_by == "2020-AD-900-01"


def test_waive_requires_reason():
    with pytest.raises(ValueError):
        make_fine().waive("  ", "2020-AD-900-01")


def test_paid_fine_cannot_be_waived():
    fine = make_fine()
    fine.pay()
    with pytest.raises(BusinessRuleError):
        fine.waive("Too late", "2020-AD-900-01")


def test_waived_fine_cannot_be_paid():
    fine = make_fine()
    fine.waive("Reason", "2020-AD-900-01")
    with pytest.raises(BusinessRuleError):
        fine.pay()
