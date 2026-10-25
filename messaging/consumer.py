import logging

from aiokafka import AIOKafkaConsumer
from pydantic import ValidationError

from app.core.config import settings
from app.core.db_helper import db_helper
from schemas.kafka import RoomBookingCommand
from services import booking_service

from .producer import EventProducer

log = logging.getLogger(__name__)

TOPIC_RESERVE = "hotel.reserve"
TOPIC_CANCEL = "hotel.cancel"


async def consume(producer: EventProducer) -> None:
    consumer = AIOKafkaConsumer(
        TOPIC_RESERVE,
        TOPIC_CANCEL,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id="hotel-service",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for msg in consumer:
            try:
                cmd = RoomBookingCommand.model_validate_json(msg.value)
            except ValidationError as exc:
                log.error("Некорректное сообщение в %s: %s", msg.topic, exc)
                await consumer.commit()
                continue

            async with db_helper.AsyncSession() as session:
                if msg.topic == TOPIC_RESERVE:
                    booking = await booking_service.reserve_room(session, cmd)
                else:
                    booking = await booking_service.cancel_room(session, cmd)

            if booking is None:
                log.warning("Команда %s не обработана: %s", msg.topic, cmd)
            else:
                await producer.send_status(booking)

            await consumer.commit()
    finally:
        await consumer.stop()