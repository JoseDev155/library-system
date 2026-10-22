from dataclasses import dataclass
from datetime import datetime


# EN: Append-only record of a system action; never edited.
# ES: Registro de una acción del sistema; solo se agrega, nunca se edita.
@dataclass(frozen=True, slots=True)
class AuditLog:
    id: int | None
    user_id: str | None
    action: str
    entity: str
    entity_id: str
    created_at: datetime
