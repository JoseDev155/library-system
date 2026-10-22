from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class Payment:
    """Payment of one fine inside a receipt. A fine is paid only once."""

    id: int | None
    receipt_id: int | None
    fine_id: int
    amount: Decimal

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise ValueError("Payment amount must be positive")
