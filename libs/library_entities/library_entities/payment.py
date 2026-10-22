from decimal import Decimal


class Payment:
    """Payment of one fine inside a receipt. A fine is paid only once."""

    def __init__(
        self, id: int | None, receipt_id: int | None, fine_id: int, amount: Decimal
    ) -> None:
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        self.id = id
        self.receipt_id = receipt_id
        self.fine_id = fine_id
        self.amount = amount
