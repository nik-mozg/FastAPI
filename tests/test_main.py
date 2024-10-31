# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client: TestClient = TestClient(app)


def test_main_route() -> None:
    """Проверка корневого маршрута приложения"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message":
        "Welcome to the Culinary Book API. Visit /docs for API documentation."}


def test_docs_route() -> None:
    """Проверка доступа к документации API по адресу /docs"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "openapi" in response.text


def test_openapi_json() -> None:
    """Проверка доступности спецификации OpenAPI в формате JSON"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"


def test_list_recipes_empty() -> None:
    """Проверка получения списка рецептов при пустой базе"""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert response.json() == []
