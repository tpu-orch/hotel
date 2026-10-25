from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RoomBookingCommand(BaseModel):
    model_config = ConfigDict(extra="allow")
    compositeBookingld: int 
    roomId: int
    arrivalDate: datetime
    departureDate: datetime


class ReservationStatusChangedPauload(BaseModel):
    model_config = ConfigDict(extra="allow")
    compositeBookingld: int
    bookingId: str
    roomId: int
    reservationStatus: str