from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .reservationStatus import ReservationStatus


class BookingStatusResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    bookingId: int
    roomId: int
    reservationStatus: ReservationStatus
    arrivalDate: datetime
    departureDate: datetime
    updatedAt: datetime | None = None