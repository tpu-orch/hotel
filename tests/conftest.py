import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api_v1 import router
from app.core.db_helper import db_helper
from app.core.exceptions import register_exception_handlers


@pytest.fixture
def client():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(router)

    async def fake_db():
        yield None

    app.dependency_overrides[db_helper.get_db] = fake_db
    return TestClient(app)