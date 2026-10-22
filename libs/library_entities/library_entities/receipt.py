from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from .exceptions import BusinessRuleError
from .payment import Payment


class PaymentMethod(StrEnum):
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"


class Receipt:
    """Cash receipt that can cover several fines (spec, RF-17)."""

    def __init__(
        self,
        id: int | None,
        receipt_number: str,
        cashier_id: str,
        method: PaymentMethod,
        paid_at: datetime,
        payments: list[Payment] | None = None,
    ) -> None:
        if not receipt_number.strip():
            raise ValueError("Receipt number cannot be empty")
        self.id = id
        self.receipt_number = receipt_number
        self.cashier_id = cashier_id
        self.method = PaymentMethod(method)
        self.paid_at = paid_at
        self.payments: list[Payment] = list(payments or [])

    @property
    def total(self) -> Decimal:
        return sum((p.amount for p in self.payments), Decimal("0.00"))

    def add_payment(self, payment: Payment) -> None:
        if any(p.fine_id == payment.fine_id for p in self.payments):
            raise BusinessRuleError("Fine already included in this receipt")
        self.payments.append(payment)
