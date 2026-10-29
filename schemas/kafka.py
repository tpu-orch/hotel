from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .reservationStatus import ReservationStatus


class RoomBookingCommand(BaseModel):
    model_config = ConfigDict(extra="allow") 

    compositeBookingId: int
    roomId: int
    arrivalDate: datetime
    departureDate: datetime


class ReservationStatusChangedPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    compositeBookingId: int
    bookingId: int
    roomId: int
    reservationStatus: ReservationStatus