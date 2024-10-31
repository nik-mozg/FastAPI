# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Создаёт таблицы перед запуском всех тестов и удаляет
    их после завершения."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Фикстура для клиента FastAPI."""
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def db_session():
    """Фикстура для создания и управления сессией базы
    данных для каждого теста."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
