# schemas.py
from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    """
    Базовая модель для представления рецепта.

    Атрибуты:
        title (str): Название блюда.
        cooking_time (int): Время приготовления в минутах.
        ingredients (str): Список ингредиентов.
        description (str): Описание способа приготовления.
    """

    title: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    """
    Модель для создания нового рецепта. Наследуется от RecipeBase.
    Используется при создании записи в базе данных.
    """

    pass


class Recipe(RecipeBase):
    """
    Модель рецепта для ответа API, включает в себя поля:

    id (int): Уникальный идентификатор рецепта.
    views (int): Количество просмотров рецепта.
    """

    id: int
    views: int
    class Config:  # Добавьте этот блок
        orm_mode = True  # Включите режим ORM
