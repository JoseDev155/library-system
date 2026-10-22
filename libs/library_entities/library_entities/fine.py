from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import StrEnum

from .exceptions import BusinessRuleError

_CENTS = Decimal("0.01")


class FineStatus(StrEnum):
    PENDING = "PENDING"
    PAID = "PAID"
    WAIVED = "WAIVED"


@dataclass(slots=True)
class Fine:
    """Fine for a late return. Amounts are USD with two decimals."""

    id: int | None
    loan_id: int
    user_id: str
    days_late: int
    rate_per_day: Decimal
    amount: Decimal
    status: FineStatus = FineStatus.PENDING
    waiver_reason: str | None = None
    waived_by: str | None = None

    def __post_init__(self) -> None:
        if self.days_late <= 0:
            raise ValueError("A fine needs at least one day late")
        if self.rate_per_day < 0 or self.amount < 0:
            raise ValueError("Rate and amount cannot be negative")
        self.status = FineStatus(self.status)

    @classmethod
    def for_late_loan(
        cls, loan_id: int, user_id: str, days_late: int, rate_per_day: Decimal
    ) -> Fine:
        # EN: Keeps the rate in force at return time.
        # ES: Conserva la tarifa vigente al devolver.
        amount = (rate_per_day * days_late).quantize(_CENTS, ROUND_HALF_UP)
        return cls(None, loan_id, user_id, days_late, rate_per_day, amount)

    def is_pending(self) -> bool:
        return self.status is FineStatus.PENDING

    def pay(self) -> None:
        if not self.is_pending():
            raise BusinessRuleError("Only a pending fine can be paid")
        self.status = FineStatus.PAID

    def waive(self, reason: str, waived_by: str) -> None:
        if not self.is_pending():
            raise BusinessRuleError("Only a pending fine can be waived")
        if not reason.strip():
            raise ValueError("A waiver needs a reason")
        self.waiver_reason = reason
        self.waived_by = waived_by
        self.status = FineStatus.WAIVED
