from datetime import UTC, datetime, timedelta

import pytest

from library_entities import BusinessRuleError, Reservation, ReservationStatus

NOW = datetime(2024, 3, 1, 10, 0, tzinfo=UTC)


def make_reservation(**overrides):
    data = {
        "id": None,
        "book_id": 1,
        "user_id": "2024-PM-101-01",
        "created_at": NOW,
    }
    data.update(overrides)
    return Reservation(**data)


def held_reservation():
    reservation = make_reservation()
    reservation.hold(copy_id=5, held_until=NOW + timedelta(hours=48))
    return reservation


def test_new_reservation_is_queued_and_active():
    reservation = make_reservation()
    assert reservation.status is ReservationStatus.QUEUED
    assert reservation.is_active()


def test_status_string_is_converted():
    assert make_reservation(status="HELD").status is ReservationStatus.HELD


def test_hold_assigns_copy_and_deadline():
    reservation = held_reservation()
    assert reservation.status is ReservationStatus.HELD
    assert reservation.copy_id == 5
    assert reservation.held_until == NOW + timedelta(hours=48)


def test_only_queued_reservation_can_be_held():
    with pytest.raises(BusinessRuleError):
        held_reservation().hold(copy_id=6, held_until=NOW)


def test_fulfill_held_reservation():
    reservation = held_reservation()
    reservation.fulfill()
    assert reservation.status is ReservationStatus.FULFILLED
    assert not reservation.is_active()


def test_queued_reservation_cannot_be_fulfilled():
    with pytest.raises(BusinessRuleError):
        make_reservation().fulfill()


def test_cancel_active_reservation():
    reservation = make_reservation()
    reservation.cancel()
    assert reservation.status is ReservationStatus.CANCELLED


def test_cancelled_reservation_cannot_be_cancelled_again():
    reservation = make_reservation()
    reservation.cancel()
    with pytest.raises(BusinessRuleError):
        reservation.cancel()


def test_expire_after_hold_period():
    reservation = held_reservation()
    reservation.expire(NOW + timedelta(hours=48))
    assert reservation.status is ReservationStatus.EXPIRED


def test_cannot_expire_before_hold_period_ends():
    with pytest.raises(BusinessRuleError):
        held_reservation().expire(NOW + timedelta(hours=1))


def test_only_held_reservation_can_expire():
    with pytest.raises(BusinessRuleError):
        make_reservation().expire(NOW)


def test_held_without_deadline_cannot_expire():
    reservation = make_reservation(status=ReservationStatus.HELD)
    with pytest.raises(BusinessRuleError):
        reservation.expire(NOW)
