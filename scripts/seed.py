import asyncio
from datetime import datetime, timezone

from sqlalchemy import select

from app.core.db_helper import db_helper
from app.core.models.bookings import Booking
from app.core.models.hotels import Hotel
from app.core.models.rooms import Room
from schemas.reservationStatus import ReservationStatus


HOTELS = [
    ("Neva Palace", "Saint Petersburg", 4, 59.9343, 30.3351),
    ("Grand Moscow", "Moscow", 5, 55.7558, 37.6173),
    ("Black Sea Resort", "Sochi", 4, 43.5855, 39.7203),
    ("Kazan Kremlin Hotel", "Kazan", 4, 55.7983, 49.1064),
    ("Siberia Grand", "Novosibirsk", 4, 55.0302, 82.9204),
    ("Amber Coast Hotel", "Kaliningrad", 4, 54.7104, 20.4522),
    ("Ural Palace", "Yekaterinburg", 4, 56.8389, 60.6057),
]


ROOMS = [
    ("101", 2, 4500),
    ("102", 3, 6500),
    ("201", 4, 12000),
]


def dt(day: int, hour: int) -> datetime:
    """Дата в октябре 2026 с часовым поясом UTC (как в примерах документации)."""
    return datetime(2026, 10, day, hour, tzinfo=timezone.utc)


S = ReservationStatus

BOOKINGS = [
    ("Grand Moscow", "101", S.RESERVED, dt(15, 14), dt(18, 12), 100001),
    ("Grand Moscow", "102", S.CANCELLED, dt(15, 14), dt(18, 12), 100002),
    ("Grand Moscow", "201", S.RESERVED, dt(12, 14), dt(15, 14), 100003),
    ("Neva Palace", "101", S.RESERVATION_PENDING, dt(20, 14), dt(22, 12), 100004),
    ("Black Sea Resort", "102", S.CANCELLATION_PENDING, dt(25, 14), dt(28, 12), 100005),
    ("Kazan Kremlin Hotel", "201", S.RESERVED, dt(10, 14), dt(13, 12), 100006),
]


async def seed_hotels_and_rooms(session) -> None:
    if await session.scalar(select(Hotel.id).limit(1)) is not None:
        print("Отели уже есть, пропускаю.")
        return

    for name, city, stars, lat, lon in HOTELS:
        hotel = Hotel(name=name, city=city, stars=stars, latitude=lat, longitude=lon)
        session.add(hotel)
        await session.flush()  # чтобы появился hotel.id

        for number, guests, price in ROOMS:
            session.add(
                Room(
                    hotelId=hotel.id,
                    roomNumber=number,
                    guestsCount=guests,
                    pricePerNight=price,
                )
            )
    await session.flush()
    print(f"Отелей: {len(HOTELS)}, номеров: {len(HOTELS) * len(ROOMS)}")


async def seed_bookings(session) -> None:
    if await session.scalar(select(Booking.bookingId).limit(1)) is not None:
        print("Брони уже есть, пропускаю.")
        return

    for hotel_name, number, status, arrival, departure, composite_id in BOOKINGS:
        room_id = await session.scalar(
            select(Room.id)
            .join(Hotel, Hotel.id == Room.hotelId)
            .where(Hotel.name == hotel_name, Room.roomNumber == number)
        )
        if room_id is None:
            raise SystemExit(f"Не найден номер {number} в отеле {hotel_name}")

        session.add(
            Booking(
                roomId=room_id,
                reservationStatus=status.value,
                arrivalDate=arrival,
                departureDate=departure,
                compositeBookingId=composite_id,
            )
        )
    await session.flush()
    print(f"Броней: {len(BOOKINGS)}")


async def seed() -> None:
    async with db_helper.AsyncSession() as session:
        await seed_hotels_and_rooms(session)
        await seed_bookings(session)
        await session.commit()

    await db_helper.engine.dispose()
    print("Готово.")


if __name__ == "__main__":
    asyncio.run(seed())