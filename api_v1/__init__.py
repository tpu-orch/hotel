from fastapi import APIRouter

from . import bookings, cities, hotels

router = APIRouter()
router.include_router(cities.router)
router.include_router(hotels.router)
router.include_router(bookings.router)