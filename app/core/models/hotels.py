from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint, UniqueConstraint
from .Base import Base

class Hotel(Base):
    __tablename__ = "hotels"
    __table_args__ = (
            CheckConstraint("stars BETWEEN 1 AND 5", name="ck_hotels_stars"),
            CheckConstraint("latitude BETWEEN -90 AND 90", name="ck_hotels_latitude"),
            CheckConstraint("longitude BETWEEN -180 AND 180", name="ck_hotels_longitude"),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    city: Mapped[str] = mapped_column()
    stars: Mapped[int] = mapped_column()
    latitude: Mapped[float | None] = mapped_column()
    longitude: Mapped[float | None] = mapped_column()