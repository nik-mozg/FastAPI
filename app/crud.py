from sqlalchemy.orm import Session
from . import models, schemas
from typing import List

def get_recipes(db: Session) -> List[models.Recipe]:
    """
    Получает все рецепты, отсортированные по количеству просмотров и
    времени приготовления.

    :param db: Сессия базы данных
    :type db: Session
    :return: Список всех рецептов, отсортированный по популярности и
    времени приготовления
    :rtype: list[models.Recipe]
    """
    return (
        db.query(models.Recipe)
        .order_by(models.Recipe.views.desc(), models.Recipe.cooking_time.asc())
        .all()
    )


def get_recipe(db: Session, recipe_id: int) -> models.Recipe | None:
    """
    Получает рецепт по ID.

    :param db: Сессия базы данных
    :type db: Session
    :param recipe_id: ID рецепта
    :type recipe_id: int
    :return: Найденный рецепт или None, если рецепт не найден
    :rtype: models.Recipe | None
    """
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def create_recipe(db: Session, recipe: schemas.RecipeCreate) -> models.Recipe:
    """
    Создает новый рецепт в базе данных.

    :param db: Сессия базы данных
    :type db: Session
    :param recipe: Данные для создания нового рецепта
    :type recipe: schemas.RecipeCreate
    :return: Созданный рецепт
    :rtype: models.Recipe
    """
    db_recipe = models.Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def delete_recipe(db: Session, recipe_id: int) -> None:
    """
    Удаляет рецепт по его ID.

    :param db: Сессия базы данных
    :type db: Session
    :param recipe_id: ID рецепта для удаления
    :type recipe_id: int
    """
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
