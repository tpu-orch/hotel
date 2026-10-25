from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from schemas.bookingstatusresponse import BookingStatusResponse
from schemas.hotel import Hotel
from schemas.reservationStatus import ReservationStatus
from schemas.room import Room


def test_hotel_coordinates_are_optional():
    hotel = Hotel(id=1, name="Grand", city="Moscow", stars=5)
    assert hotel.latitude is None
    assert hotel.longitude is None


@pytest.mark.parametrize("stars", [0, 6, -1])
def test_hotel_stars_out_of_range(stars):
    with pytest.raises(ValidationError):
        Hotel(id=1, name="Grand", city="Moscow", stars=stars)


@pytest.mark.parametrize("lat", [-91, 91])
def test_hotel_latitude_out_of_range(lat):
    with pytest.raises(ValidationError):
        Hotel(id=1, name="Grand", city="Moscow", stars=5, latitude=lat)


def test_room_guests_count_must_be_positive():
    with pytest.raises(ValidationError):
        Room(id=1, hotelId=1, pricePerNight=100, roomNumber="101", guestsCount=0)


def test_room_price_cannot_be_negative():
    with pytest.raises(ValidationError):
        Room(id=1, hotelId=1, pricePerNight=-1, roomNumber="101", guestsCount=2)


def test_reservation_status_has_five_values_from_spec():
    assert {s.value for s in ReservationStatus} == {
        "AVAILABLE",
        "RESERVATION_PENDING",
        "RESERVED",
        "CANCELLATION_PENDING",
        "CANCELLED",
    }


def test_booking_status_rejects_unknown_status():
    with pytest.raises(ValidationError):
        BookingStatusResponse(
            bookingId=1,
            roomId=1,
            reservationStatus="CONFIRMED",
            arrivalDate=datetime(2026, 10, 15, tzinfo=timezone.utc),
            departureDate=datetime(2026, 10, 18, tzinfo=timezone.utc),
        )


def test_booking_status_can_be_built_from_db_object():
    booking = SimpleNamespace(
        bookingId=1,
        roomId=2,
        reservationStatus="RESERVED",
        arrivalDate=datetime(2026, 10, 15, tzinfo=timezone.utc),
        departureDate=datetime(2026, 10, 18, tzinfo=timezone.utc),
        updatedAt=None,
    )
    response = BookingStatusResponse.model_validate(booking)
    assert response.reservationStatus == ReservationStatus.RESERVED
    assert response.updatedAt is None