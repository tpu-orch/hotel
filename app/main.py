from fastapi import FastAPI


import asyncio
from contextlib import asynccontextmanager, suppress



from api_v1 import router as api_v1_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from messaging.consumer import consume
from messaging.producer import EventProducer



@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = EventProducer(settings.kafka_bootstrap_servers)
    await producer.start()
    task = asyncio.create_task(consume(producer))
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
    await producer.stop()



app = FastAPI(
    title="Сервис отелей",
    version="1.0.0",
    description=(
        "Тестовый сервис отелей для взаимодействия с сервисом оркестрации путешествий. "
        "HTTP API: поиск городов, отелей, доступных номеров и статус бронирования. "
        "Бронирование и отмена выполняются асинхронно через Kafka."
    ),
)

register_exception_handlers(app)
app.include_router(api_v1_router)