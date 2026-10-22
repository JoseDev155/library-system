from datetime import datetime
from enum import StrEnum

from .exceptions import BusinessRuleError


class ReservationStatus(StrEnum):
    QUEUED = "QUEUED"
    HELD = "HELD"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class Reservation:
    """User reservation of a book, queued until a copy is held."""

    def __init__(
        self,
        id: int | None,
        book_id: int,
        user_id: str,
        created_at: datetime,
        copy_id: int | None = None,
        status: ReservationStatus = ReservationStatus.QUEUED,
        held_until: datetime | None = None,
    ) -> None:
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.copy_id = copy_id
        self.created_at = created_at
        self.status = ReservationStatus(status)
        self.held_until = held_until

    def is_active(self) -> bool:
        return self.status in (ReservationStatus.QUEUED, ReservationStatus.HELD)

    def hold(self, copy_id: int, held_until: datetime) -> None:
        if self.status is not ReservationStatus.QUEUED:
            raise BusinessRuleError("Only a queued reservation can be held")
        self.copy_id = copy_id
        self.held_until = held_until
        self.status = ReservationStatus.HELD

    def fulfill(self) -> None:
        if self.status is not ReservationStatus.HELD:
            raise BusinessRuleError("Only a held reservation can be fulfilled")
        self.status = ReservationStatus.FULFILLED

    def cancel(self) -> None:
        if not self.is_active():
            raise BusinessRuleError("Reservation is no longer active")
        self.status = ReservationStatus.CANCELLED

    def expire(self, now: datetime) -> None:
        if self.status is not ReservationStatus.HELD:
            raise BusinessRuleError("Only a held reservation can expire")
        if self.held_until is None or now < self.held_until:
            raise BusinessRuleError("Hold period has not ended")
        self.status = ReservationStatus.EXPIRED
