from aiokafka import AIOKafkaProducer

from app.core.models.bookings import Booking
from schemas.kafka import ReservationStatusChangedPayload

TOPIC_STATUS = "hotel.reservation-status"


class EventProducer:
    def __init__(self, bootstrap_servers: str):
        self._producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self) -> None:
        await self._producer.start()

    async def stop(self) -> None:
        await self._producer.stop()

    async def send_status(self, booking: Booking) -> None:
        payload = ReservationStatusChangedPayload(
            compositeBookingId=booking.compositeBookingId,
            bookingId=booking.bookingId,
            roomId=booking.roomId,
            reservationStatus=booking.reservationStatus,
        )
        await self._producer.send_and_wait(
            TOPIC_STATUS,
            key=str(booking.compositeBookingId).encode(),
            value=payload.model_dump_json().encode(),
        )