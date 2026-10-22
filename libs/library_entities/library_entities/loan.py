from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import StrEnum

from .exceptions import BusinessRuleError


class LoanStatus(StrEnum):
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"


# EN: Loan of one copy to one user.
# ES: Préstamo de un ejemplar a un usuario.
@dataclass(slots=True)
class Loan:
    id: int | None
    copy_id: int
    user_id: str
    loaned_by: str
    loaned_at: datetime
    due_at: datetime
    returned_at: datetime | None = None
    renewals: int = 0
    status: LoanStatus = LoanStatus.ACTIVE

    def __post_init__(self) -> None:
        if self.due_at <= self.loaned_at:
            raise ValueError("Due date must be after the loan date")
        self.status = LoanStatus(self.status)

    def is_active(self) -> bool:
        return self.status is LoanStatus.ACTIVE

    def is_overdue(self, now: datetime) -> bool:
        # EN: Overdue is derived from due_at, never stored.
        # ES: El vencimiento se calcula con due_at, no se guarda.
        return self.is_active() and now > self.due_at

    def renew(self, max_renewals: int, loan_days: int) -> None:
        if not self.is_active():
            raise BusinessRuleError("Only an active loan can be renewed")
        if self.renewals >= max_renewals:
            raise BusinessRuleError("Maximum renewals reached")
        self.due_at = self.due_at + timedelta(days=loan_days)
        self.renewals += 1

    def days_late(self, today: date) -> int:
        end = self.returned_at.date() if self.returned_at else today
        return max((end - self.due_at.date()).days, 0)

    def close(self, returned_at: datetime) -> None:
        if not self.is_active():
            raise BusinessRuleError("Loan is already returned")
        self.returned_at = returned_at
        self.status = LoanStatus.RETURNED
