from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from .exceptions import BusinessRuleError
from .payment import Payment


class PaymentMethod(StrEnum):
    CASH = "CASH"
    CARD = "CARD"
    TRANSFER = "TRANSFER"


@dataclass(slots=True)
class Receipt:
    """Cash receipt that can cover several fines (spec, RF-17)."""

    id: int | None
    receipt_number: str
    cashier_id: str
    method: PaymentMethod
    paid_at: datetime
    payments: list[Payment] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.method = PaymentMethod(self.method)

    @property
    def total(self) -> Decimal:
        return sum((p.amount for p in self.payments), Decimal("0.00"))

    def add_payment(self, payment: Payment) -> None:
        if any(p.fine_id == payment.fine_id for p in self.payments):
            raise BusinessRuleError("Fine already included in this receipt")
        self.payments.append(payment)
