from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.crud import ACTIVE_STATUSES
from app.core.models.bookings import Booking
from app.core.models.rooms import Room
from schemas.kafka import RoomBookingCommand
from schemas.reservationStatus import ReservationStatus



async def find_booking(session: AsyncSession, cmd: RoomBookingCommand) -> Booking | None:
    stmt = (select(Booking).where(
            Booking.compositeBookingId == cmd.compositeBookingId,
            Booking.roomId == cmd.roomId,
        )
        .order_by(Booking.bookingId.desc())
        .limit(1)
    )
    return await session.scalar(stmt)



async def reserve_room(session: AsyncSession, cmd: RoomBookingCommand) -> Booking | None:
    if cmd.departureDate <= cmd.arrivalDate:
        return None
    
    existing = await find_booking(session, cmd)
    if existing and existing.reservationStatus in ACTIVE_STATUSES:
        return existing
    
    room = await session.scalar(select(Room).where(Room.id == cmd.roomId).with_for_update())
    if room is None:
        return None
    
    overlap = await session.scalar(
        select(Booking.bookingId)
        .where(
            Booking.roomId == cmd.roomId,
            Booking.reservationStatus.in_(ACTIVE_STATUSES),
            Booking.arrivalDate < cmd.departureDate,
            Booking.departureDate > cmd.arrivalDate,
        )
        .limit(1)
    )
    status = ReservationStatus.CANCELLED if overlap else ReservationStatus.RESERVED
    
    booking = Booking(
        compositeBookingId=cmd.compositeBookingId,
        roomId=cmd.roomId,
        reservationStatus=status.value,
        arrivalDate=cmd.arrivalDate,
        departureDate=cmd.departureDate,
    )
    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    return booking



async def cancel_room(session: AsyncSession, cmd: RoomBookingCommand) -> Booking | None:
    booking = await find_booking(session, cmd)
    if booking is None:
        return None

    if booking.reservationStatus in ACTIVE_STATUSES:
        booking.reservationStatus = ReservationStatus.CANCELLED.value
        await session.commit()
        await session.refresh(booking)
    return booking