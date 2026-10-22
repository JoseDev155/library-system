from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AuditLog:
    """Append-only record of a system action; never edited."""

    id: int | None
    user_id: str | None
    action: str
    entity: str
    entity_id: str
    created_at: datetime
