<<<<<<< HEAD
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .reservationStatus import ReservationStatus


class RoomBookingCommand(BaseModel):
    model_config = ConfigDict(extra="allow") 

    compositeBookingId: int
=======
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RoomBookingCommand(BaseModel):
    model_config = ConfigDict(extra="allow")
    compositeBookingld: int 
>>>>>>> dev
    roomId: int
    arrivalDate: datetime
    departureDate: datetime


<<<<<<< HEAD
class ReservationStatusChangedPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    compositeBookingId: int
    bookingId: int
    roomId: int
    reservationStatus: ReservationStatus
=======
class ReservationStatusChangedPauload(BaseModel):
    model_config = ConfigDict(extra="allow")
    compositeBookingld: int
    bookingId: str
    roomId: int
    reservationStatus: str
>>>>>>> dev
