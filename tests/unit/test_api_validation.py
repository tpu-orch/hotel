from datetime import datetime, timezone
from types import SimpleNamespace

from api_v1 import crud

ROOMS_URL = "/hotels/1/rooms"
VALID_PARAMS = {
    "arrivalDate": "2026-10-15T14:00:00Z",
    "departureDate": "2026-10-18T12:00:00Z",
    "guestsCount": 2,
}


# ---- /cities ----

def test_cities_empty_query_returns_400(client):
    response = client.get("/cities", params={"query": ""})
    assert response.status_code == 400
    assert response.json()["code"] == "INVALID_PARAMETER"


def test_cities_too_long_query_returns_400(client):
    response = client.get("/cities", params={"query": "a" * 101})
    assert response.status_code == 400


def test_cities_returns_list_of_strings(client, monkeypatch):
    async def fake(session, query):
        return ["Moscow", "Mosul"]

    monkeypatch.setattr(crud, "search_cities", fake)
    response = client.get("/cities", params={"query": "mos"})
    assert response.status_code == 200
    assert response.json() == ["Moscow", "Mosul"]


def test_cities_nothing_found_is_200_not_error(client, monkeypatch):
    async def fake(session, query):
        return []

    monkeypatch.setattr(crud, "search_cities", fake)
    response = client.get("/cities", params={"query": "234"})
    assert response.status_code == 200
    assert response.json() == []


# ---- /hotels ----

def test_hotels_requires_city(client):
    response = client.get("/hotels")
    assert response.status_code == 400
    assert response.json()["code"] == "INVALID_PARAMETER"


# ---- /hotels/{hotelId}/rooms ----

def test_rooms_departure_before_arrival_returns_400(client):
    params = {**VALID_PARAMS, "departureDate": "2026-10-14T12:00:00Z"}
    response = client.get(ROOMS_URL, params=params)
    assert response.status_code == 400
    assert response.json()["code"] == "INVALID_PARAMETER"


def test_rooms_departure_equal_arrival_returns_400(client):
    params = {**VALID_PARAMS, "departureDate": VALID_PARAMS["arrivalDate"]}
    response = client.get(ROOMS_URL, params=params)
    assert response.status_code == 400


def test_rooms_guests_count_zero_returns_400(client):
    response = client.get(ROOMS_URL, params={**VALID_PARAMS, "guestsCount": 0})
    assert response.status_code == 400


def test_rooms_bad_date_format_returns_400(client):
    response = client.get(ROOMS_URL, params={**VALID_PARAMS, "arrivalDate": "abc"})
    assert response.status_code == 400


def test_rooms_hotel_not_found_returns_404(client, monkeypatch):
    async def fake_get_hotel(session, hotel_id):
        return None

    monkeypatch.setattr(crud, "get_hotel", fake_get_hotel)
    response = client.get("/hotels/999/rooms", params=VALID_PARAMS)
    assert response.status_code == 404
    assert response.json() == {
        "code": "HOTEL_NOT_FOUND",
        "message": "Отель с указанным ID не найден.",
    }


def test_rooms_success_uses_camel_case_fields(client, monkeypatch):
    async def fake_get_hotel(session, hotel_id):
        return SimpleNamespace(id=hotel_id)

    async def fake_search(session, hotel_id, arrival, departure, guests):
        return [
            SimpleNamespace(
                id=10, hotelId=hotel_id, pricePerNight=4500.0, roomNumber="101", guestsCount=2
            )
        ]

    monkeypatch.setattr(crud, "get_hotel", fake_get_hotel)
    monkeypatch.setattr(crud, "search_available_rooms", fake_search)

    response = client.get(ROOMS_URL, params=VALID_PARAMS)
    assert response.status_code == 200
    room = response.json()[0]
    assert room["roomNumber"] == "101"
    assert room["hotelId"] == 1
    assert room["pricePerNight"] == 4500.0


# ---- /bookings/{bookingId}/status ----

def test_booking_id_zero_returns_400(client):
    response = client.get("/bookings/0/status")
    assert response.status_code == 400


def test_booking_id_not_a_number_returns_400(client):
    response = client.get("/bookings/abc/status")
    assert response.status_code == 400


def test_booking_not_found_returns_404(client, monkeypatch):
    async def fake(session, booking_id):
        return None

    monkeypatch.setattr(crud, "get_booking_status", fake)
    response = client.get("/bookings/999/status")
    assert response.status_code == 404
    assert response.json()["code"] == "BOOKING_NOT_FOUND"


def test_booking_found_returns_status(client, monkeypatch):
    async def fake(session, booking_id):
        return SimpleNamespace(
            bookingId=booking_id,
            roomId=5,
            reservationStatus="RESERVED",
            arrivalDate=datetime(2026, 10, 15, 14, tzinfo=timezone.utc),
            departureDate=datetime(2026, 10, 18, 12, tzinfo=timezone.utc),
            updatedAt=None,
        )

    monkeypatch.setattr(crud, "get_booking_status", fake)
    response = client.get("/bookings/1/status")
    body = response.json()
    assert response.status_code == 200
    assert body["bookingId"] == 1
    assert body["reservationStatus"] == "RESERVED"