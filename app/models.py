from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Recipe(Base):
    """
    Модель таблицы 'recipes' для хранения информации о рецептах.

    Атрибуты:
        id (int): Уникальный идентификатор рецепта.
        title (str): Название блюда.
        cooking_time (int): Время приготовления в минутах.
        ingredients (str): Список ингредиентов.
        description (str): Описание способа приготовления.
        views (int): Количество просмотров рецепта, изначально 0.
    """

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cooking_time = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)
    views = Column(Integer, default=0)
