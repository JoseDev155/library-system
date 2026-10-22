import re
from enum import StrEnum

from .exceptions import BusinessRuleError

# EN: University ID format AAAA-II-FFF-NN (spec, section 8.2).
# ES: Formato del carnet AAAA-II-FFF-NN (spec, sección 8.2).
_UNIVERSITY_ID_PATTERN = re.compile(r"^[0-9]{4}-[A-Z]{2}-[0-9]{3}-[0-9]{2,}$")


class Role(StrEnum):
    ADMIN = "admin"
    DEV = "dev"
    LIBRARIAN = "librarian"
    CASHIER = "cashier"
    TEACHER = "teacher"
    STUDENT = "student"


class User:
    """System user identified by the university ID (carnet)."""

    def __init__(
        self,
        id: str,
        institutional_email: str,
        name: str,
        role: Role,
        faculty_code: str,
        active: bool = True,
    ) -> None:
        if not _UNIVERSITY_ID_PATTERN.match(id):
            raise ValueError("User id must follow the format AAAA-II-FFF-NN")
        if not institutional_email.strip():
            raise ValueError("Institutional email cannot be empty")
        if not name.strip():
            raise ValueError("User name cannot be empty")
        self.id = id
        self.institutional_email = institutional_email
        self.name = name
        self.role = Role(role)
        self.faculty_code = faculty_code
        self.active = active

    def can_log_in(self) -> bool:
        return self.active

    def can_borrow(self, has_pending_fines: bool) -> bool:
        # EN: Pending fines block loans but keep the account active.
        # ES: Las multas pendientes bloquean préstamos, pero la cuenta sigue activa.
        return self.active and not has_pending_fines

    def ensure_can_borrow(self, has_pending_fines: bool) -> None:
        if not self.active:
            raise BusinessRuleError("Inactive user cannot borrow")
        if has_pending_fines:
            raise BusinessRuleError("User has pending fines")

    def deactivate(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
