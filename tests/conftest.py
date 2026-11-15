import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient

from backend.database import SessionLocal
from backend.main import SESSIONS, app
from backend.seed import reset_demo_data


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        with SessionLocal() as db:
            reset_demo_data(db)
        SESSIONS.clear()
        yield test_client
