from dataclasses import dataclass
from enum import StrEnum

from .exceptions import BusinessRuleError


class CopyStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    LOANED = "LOANED"
    RESERVED = "RESERVED"
    UNDER_REPAIR = "UNDER_REPAIR"
    WITHDRAWN = "WITHDRAWN"


class Circulation(StrEnum):
    LOANABLE = "LOANABLE"
    REFERENCE_ONLY = "REFERENCE_ONLY"


# EN: Physical copy of a book.
# ES: Ejemplar físico de un libro.
@dataclass(slots=True)
class BookCopy:
    id: int | None
    book_id: int
    inventory_code: str
    status: CopyStatus = CopyStatus.AVAILABLE
    circulation: Circulation = Circulation.LOANABLE
    location_floor: str | None = None
    location_shelf: str | None = None

    def __post_init__(self) -> None:
        self.status = CopyStatus(self.status)
        self.circulation = Circulation(self.circulation)

    def can_be_loaned(self) -> bool:
        return self.circulation is Circulation.LOANABLE and self.status in (
            CopyStatus.AVAILABLE,
            CopyStatus.RESERVED,
        )

    def mark_loaned(self) -> None:
        if self.circulation is Circulation.REFERENCE_ONLY:
            raise BusinessRuleError("Reference-only copy cannot be loaned")
        if self.status not in (CopyStatus.AVAILABLE, CopyStatus.RESERVED):
            raise BusinessRuleError("Copy is not available for loan")
        self.status = CopyStatus.LOANED

    def mark_returned(self) -> None:
        if self.status is not CopyStatus.LOANED:
            raise BusinessRuleError("Copy is not loaned")
        self.status = CopyStatus.AVAILABLE

    def mark_reserved(self) -> None:
        if self.status is not CopyStatus.AVAILABLE:
            raise BusinessRuleError("Only an available copy can be reserved")
        self.status = CopyStatus.RESERVED

    def release_reservation(self) -> None:
        if self.status is not CopyStatus.RESERVED:
            raise BusinessRuleError("Copy is not reserved")
        self.status = CopyStatus.AVAILABLE

    def send_to_repair(self) -> None:
        if self.status is not CopyStatus.AVAILABLE:
            raise BusinessRuleError("Only an available copy can go to repair")
        self.status = CopyStatus.UNDER_REPAIR

    def finish_repair(self) -> None:
        if self.status is not CopyStatus.UNDER_REPAIR:
            raise BusinessRuleError("Copy is not under repair")
        self.status = CopyStatus.AVAILABLE

    def withdraw(self) -> None:
        if self.status is CopyStatus.LOANED:
            raise BusinessRuleError("A loaned copy cannot be withdrawn")
        self.status = CopyStatus.WITHDRAWN
