from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from library_entities import AuditLog


def make_entry():
    return AuditLog(
        id=None,
        user_id="2020-AD-900-01",
        action="FINE_WAIVED",
        entity="Fine",
        entity_id="7",
        created_at=datetime(2024, 3, 10, 12, 0, tzinfo=UTC),
    )


def test_audit_log_is_append_only():
    entry = make_entry()
    with pytest.raises(FrozenInstanceError):
        entry.action = "OTHER"


def test_user_can_be_missing_for_system_actions():
    entry = AuditLog(
        None, None, "JOB", "Loan", "1", datetime(2024, 1, 1, tzinfo=UTC)
    )
    assert entry.user_id is None
