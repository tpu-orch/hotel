from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint

from .Base import Base

class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        CheckConstraint('"pricePerNight" >= 0', name="ck_rooms_price"),
        CheckConstraint('"guestsCount" >= 1', name="ck_rooms_guests"),
        UniqueConstraint("hotelId", "roomNumber", name="uq_rooms_hotel_number"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hotelId: Mapped[int] = mapped_column(ForeignKey("hotels.id"), index=True)
    pricePerNight: Mapped[float] = mapped_column()
    roomNumber: Mapped[str] = mapped_column()
    guestsCount: Mapped[int] = mapped_column()