from fastapi import FastAPI
from .endpoints import recipes
from .database import init_db

app = FastAPI(
    title="Culinary Book API",
    description=(
        "API для управления рецептами. Позволяет создавать, читать, "
        "обновлять и удалять рецепты. Полный список маршрутов и их "
        "описания доступен на /docs."
    ),
    version="1.0.0"
)


# Инициализация базы данных перед запуском
init_db()

# Подключаем маршруты для работы с рецептами
app.include_router(recipes.router, tags=["recipes"])


@app.get("/", summary="Корневой маршрут",
         response_description="Сообщение приветствия для пользователя")
def read_root() -> dict:
    """
    Корневой маршрут приложения.

    :return: Сообщение приветствия с ссылкой на документацию API.
    """
    return {
        "message": (
            "Welcome to the Culinary Book API. "
            "Visit /docs for API documentation."
        )
    }
