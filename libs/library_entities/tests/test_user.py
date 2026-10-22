import pytest

from library_entities import BusinessRuleError, Role, User


def make_user(**overrides):
    data = {
        "id": "2024-PM-101-01",
        "institutional_email": "juan@uni.edu",
        "name": "Juan Pérez",
        "role": Role.STUDENT,
        "faculty_code": "101",
    }
    data.update(overrides)
    return User(**data)


@pytest.mark.parametrize(
    "user_id", ["2024-PM-101-01", "2024-PX-900-12", "1999-AB-301-100"]
)
def test_valid_university_ids(user_id):
    assert make_user(id=user_id).id == user_id


@pytest.mark.parametrize(
    "user_id",
    [
        "",
        "2024-PM-101",
        "24-PM-101-01",
        "2024-pm-101-01",
        "2024-PM-10-01",
        "2024-PM-101-1",
    ],
)
def test_invalid_university_ids(user_id):
    with pytest.raises(ValueError):
        make_user(id=user_id)


def test_role_string_is_converted_to_enum():
    assert make_user(role="teacher").role is Role.TEACHER


def test_invalid_role_is_rejected():
    with pytest.raises(ValueError):
        make_user(role="visitor")


def test_active_user_can_log_in_and_borrow():
    user = make_user()
    assert user.can_log_in()
    assert user.can_borrow(has_pending_fines=False)
    user.ensure_can_borrow(has_pending_fines=False)


def test_pending_fines_block_borrowing_but_not_login():
    user = make_user()
    assert user.can_log_in()
    assert not user.can_borrow(has_pending_fines=True)
    with pytest.raises(BusinessRuleError):
        user.ensure_can_borrow(has_pending_fines=True)


def test_inactive_user_cannot_log_in_or_borrow():
    user = make_user(active=False)
    assert not user.can_log_in()
    assert not user.can_borrow(has_pending_fines=False)
    with pytest.raises(BusinessRuleError):
        user.ensure_can_borrow(has_pending_fines=False)


def test_deactivate_and_activate():
    user = make_user()
    user.deactivate()
    assert not user.active
    user.activate()
    assert user.active
