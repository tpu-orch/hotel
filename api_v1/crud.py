from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.bookings import Booking
from app.core.models.hotels import Hotel
from app.core.models.rooms import Room
from schemas.reservationStatus import ReservationStatus
from app.core.rules import ACTIVE_STATUSES


async def search_cities(session: AsyncSession, query: str | None) -> list[str]:
    stmt = select(Hotel.city).distinct().order_by(Hotel.city)
    if query:
        stmt = stmt.where(Hotel.city.ilike(f"%{query}%"))
    return list(await session.scalars(stmt))



async def search_hotels(session: AsyncSession, city: str) -> list[Hotel]:
    stmt = (
        select(Hotel)
        .where(func.lower(Hotel.city) == city.lower())
        .order_by(Hotel.id)
    )
    return list(await session.scalars(stmt))



async def search_available_rooms(
    session: AsyncSession,
    hotel_id: int,
    arrival: datetime,
    departure: datetime,
    guests: int,
) -> list[Room]:
    overlapping = select(Booking.bookingId).where(
        Booking.roomId == Room.id,
        Booking.reservationStatus.in_(ACTIVE_STATUSES),
        Booking.arrivalDate < departure,
        Booking.departureDate > arrival,
    )
    stmt = (
        select(Room)
        .where(
            Room.hotelId == hotel_id,
            Room.guestsCount >= guests,
            ~overlapping.exists(),
        )
        .order_by(Room.pricePerNight)
    )
    return list(await session.scalars(stmt))



async def get_hotel(session: AsyncSession, hotel_id: int) -> Hotel | None:
    return await session.get(Hotel, hotel_id)



async def get_booking_status(session: AsyncSession, bookingId: int) -> Booking | None:
    return await session.get(Booking, bookingId)