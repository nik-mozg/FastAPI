# tests/test_recipes.py
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def recipe_data() -> dict:
    """Создаёт тестовые данные для рецепта."""
    return {
        "title": "Pasta",
        "cooking_time": 15,
        "ingredients": "Pasta, Tomato Sauce",
        "description": "Boil pasta and add sauce."
    }


def test_create_recipe(client: TestClient, recipe_data: dict) -> None:
    """Тестирует создание рецепта и проверяет ответ."""
    response = client.post("/recipes", json=recipe_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Pasta"


def test_get_recipe(client: TestClient) -> None:
    """Тестирует получение рецепта и увеличение счетчика просмотров."""
    recipe_data = {
        "title": "Salad",
        "cooking_time": 10,
        "ingredients": "Lettuce, Tomato, Cucumber",
        "description": "Mix vegetables and season with salt."
    }
    post_response = client.post("/recipes", json=recipe_data)
    recipe_id = post_response.json()["id"]

    # Проверка получения рецепта
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Salad"
    assert get_response.json()["views"] == 1  # Первый просмотр

    # Повторный запрос для увеличения счетчика
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 200
    assert get_response.json()["views"] == 2  # Второй просмотр


def test_update_recipe(client: TestClient) -> None:
    """Тестирует обновление рецепта и проверяет изменения в ответе."""
    recipe_data = {
        "title": "Soup",
        "cooking_time": 20,
        "ingredients": "Chicken, Vegetables, Broth",
        "description": "Cook ingredients in broth."
    }
    post_response = client.post("/recipes", json=recipe_data)
    recipe_id = post_response.json()["id"]

    updated_data = {
        "title": "Vegetable Soup",
        "cooking_time": 25,
        "ingredients": "Vegetables, Broth",
        "description": "Boil vegetables in broth."
    }
    response = client.put(f"/recipes/{recipe_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Vegetable Soup"
    assert response.json()["cooking_time"] == 25


def test_delete_recipe(client: TestClient) -> None:
    """Тестирует удаление рецепта и проверяет отсутствие рецепта в базе."""
    recipe_data = {
        "title": "Smoothie",
        "cooking_time": 5,
        "ingredients": "Banana, Milk, Honey",
        "description": "Blend all ingredients."
    }
    post_response = client.post("/recipes", json=recipe_data)
    recipe_id = post_response.json()["id"]

    # Удаление рецепта
    delete_response = client.delete(f"/recipes/{recipe_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Рецепт удален"

    # Проверка отсутствия рецепта
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404


def test_get_all_recipes(client: TestClient, recipe_data: dict) -> None:
    """Тестирует получение всех рецептов и сортировку по просмотрам."""
    # Создаем несколько рецептов
    client.post("/recipes", json=recipe_data)
    recipe_data["title"] = "Salad"
    client.post("/recipes", json=recipe_data)

    # Проверка получения всех рецептов
    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) >= 2  # Убедимся, что создано минимум два рецепта
    # Проверка сортировки по просмотрам
    assert recipes[0]["views"] >= recipes[1]["views"]
