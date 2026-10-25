from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, func
from datetime import datetime

from .Base import Base

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint('"departureDate" > "arrivalDate"', name="ck_bookings_dates"),
    )
    
    
    bookingId: Mapped[int] = mapped_column(primary_key=True)
    roomId: Mapped[int] = mapped_column(ForeignKey("rooms.id"), index=True)
    compositeBookingId: Mapped[int | None] = mapped_column(index=True)
    reservationStatus: Mapped[str] = mapped_column()
    arrivalDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    departureDate: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updatedAt: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )