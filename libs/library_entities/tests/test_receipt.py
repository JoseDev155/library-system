from datetime import UTC, datetime
from decimal import Decimal

import pytest

from library_entities import BusinessRuleError, Payment, PaymentMethod, Receipt

PAID_AT = datetime(2024, 3, 10, 12, 0, tzinfo=UTC)


def make_receipt(**overrides):
    data = {
        "id": None,
        "receipt_number": "R-0001",
        "cashier_id": "2020-CA-900-01",
        "method": PaymentMethod.CASH,
        "paid_at": PAID_AT,
    }
    data.update(overrides)
    return Receipt(**data)


def test_empty_receipt_total_is_zero():
    assert make_receipt().total == Decimal("0.00")


def test_method_string_is_converted():
    assert make_receipt(method="CARD").method is PaymentMethod.CARD


def test_invalid_method_is_rejected():
    with pytest.raises(ValueError):
        make_receipt(method="CRYPTO")


def test_total_is_sum_of_payments():
    receipt = make_receipt()
    receipt.add_payment(Payment(None, None, 1, Decimal("0.75")))
    receipt.add_payment(Payment(None, None, 2, Decimal("1.50")))
    assert receipt.total == Decimal("2.25")


def test_same_fine_cannot_appear_twice():
    receipt = make_receipt()
    receipt.add_payment(Payment(None, None, 1, Decimal("0.75")))
    with pytest.raises(BusinessRuleError):
        receipt.add_payment(Payment(None, None, 1, Decimal("0.75")))


def test_receipts_do_not_share_payment_lists():
    first = make_receipt()
    second = make_receipt()
    first.add_payment(Payment(None, None, 1, Decimal("1.00")))
    assert second.payments == []


def test_payment_amount_must_be_positive():
    with pytest.raises(ValueError):
        Payment(None, None, 1, Decimal(0))
    with pytest.raises(ValueError):
        Payment(None, None, 1, Decimal(-1))
