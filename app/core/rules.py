from datetime import datetime

from schemas.reservationStatus import ReservationStatus

ACTIVE_STATUSES = (
    ReservationStatus.RESERVATION_PENDING.value,
    ReservationStatus.RESERVED.value,
    ReservationStatus.CANCELLATION_PENDING.value,
)


def occupies_room(status: str) -> bool:
    return status in ACTIVE_STATUSES


def periods_overlap(
    a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime
) -> bool:
    return a_start < b_end and a_end > b_start