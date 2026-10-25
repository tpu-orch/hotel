from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.exceptions import ApiError
from schemas.bookingstatusresponse import BookingStatusResponse
from schemas.error import Error

from . import crud

router = APIRouter(prefix="/bookings", tags=["Бронирование"],)



@router.get(
    "/{bookingId}/status",
    response_model=BookingStatusResponse,
    summary="Получить статус бронирования",
    operation_id="getBookingStatus",
    responses={
        200: {"description": "Текущий статус бронирования."},
        400: {"model": Error, "description": "Некорректный идентификатор бронирования."},
        404: {"model": Error, "description": "Бронирование не найдено."},
    },
)
async def get_booking_status(
    bookingId: int = Path(..., ge=1, description="Внутренний идентификатор бронирования."),
    session: AsyncSession = Depends(db_helper.get_db),
):

    booking = await crud.get_booking_status(session, bookingId)

    if booking is None:
        raise ApiError(404, "BOOKING_NOT_FOUND", "Бронирование с указанным ID не найдено.")
    return booking