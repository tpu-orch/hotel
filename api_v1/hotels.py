from datetime import datetime

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.exceptions import ApiError
from schemas.error import Error
from schemas.hotel import Hotel
from schemas.room import Room

from . import crud

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    response_model=list[Hotel],
    tags=["Отели"],
    summary="Поиск отелей по городу",
    operation_id="searchHotels",
    responses={
        200: {"description": "Список отелей в указанном городе."},
        400: {"model": Error, "description": "Не указан город или его значение некорректно."},
    },
)
async def search_hotels(
    city: str = Query(..., min_length=1, max_length=100, description="Название города, в котором ищутся отели."),
    session: AsyncSession = Depends(db_helper.get_db),
):
    
    return await crud.search_hotels(session, city)


@router.get(
    "/{hotelId}/rooms",
    response_model=list[Room],
    tags=["Комнаты"],
    summary="Поиск доступных номеров",
    operation_id="searchAvailableRooms",
    responses={
        200: {"description": "Список подходящих номеров. Может быть пустым."},
        400: {"model": Error, "description": "Некорректные даты или количество гостей."},
        404: {"model": Error, "description": "Отель с указанным идентификатором не найден."},
    },
)
async def search_available_rooms(
    hotelId: int = Path(..., ge=1, description="Идентификатор отеля."),
    arrivalDate: datetime = Query(..., description="Дата и время заезда в формате ISO 8601."),
    departureDate: datetime = Query(..., description="Дата и время выезда в формате ISO 8601."),
    guestsCount: int = Query(..., ge=1, description="Минимальная вместимость номера."),
    session: AsyncSession = Depends(db_helper.get_db),
):
    
    if departureDate <= arrivalDate:
        raise ApiError(400, "INVALID_PARAMETER", "Дата выезда должна быть позже даты заезда.")

    hotel = await crud.get_hotel(session, hotelId)
    if hotel is None:
        raise ApiError(404, "HOTEL_NOT_FOUND", "Отель с указанным ID не найден.")

    return await crud.search_available_rooms(
        session, hotelId, arrivalDate, departureDate, guestsCount
    )