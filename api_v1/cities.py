from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from schemas.error import Error

from . import crud

router = APIRouter(prefix="/cities", tags=["Города"])


@router.get(
    "",
    response_model=list[str],
    summary="Поиск городов",
    operation_id="searchCities",
    responses={
        200: {"description": "Список найденных городов. Может быть пустым."},
        400: {"model": Error, "description": "Некорректный параметр query."},
    },
)
async def search_cities(
    query: str | None = Query(
        None,
        min_length=1,
        max_length=100,
        description="Часть названия города для поиска.",
    ),
    session: AsyncSession = Depends(db_helper.get_db),
):
    
    return await crud.search_cities(session, query)