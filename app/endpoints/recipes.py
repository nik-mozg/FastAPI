# recipes.py
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from typing import List, Dict
from app import crud, schemas, models, database


router = APIRouter()


@router.get(
    "/recipes",
    response_model=List[schemas.Recipe],
    summary="Получить все рецепты",
    description=(
        "Возвращает список всех рецептов, отсортированный по количеству "
        "просмотров и времени приготовления."
    ),
)
def read_recipes(db: Session = Depends(database.get_db)) -> List[schemas.Recipe]:
    """
    Возвращает список всех рецептов, отсортированный по
    популярности (по количеству просмотров) и времени приготовления.
    """
    return crud.get_recipes(db)


@router.get(
    "/recipes/{recipe_id}",
    response_model=schemas.Recipe,
    summary="Получить рецепт по ID",
    description=(
        "Возвращает информацию о конкретном рецепте и "
        "увеличивает счетчик просмотров."
    ),
)
def read_recipe(
    recipe_id: int = Path(..., description="ID рецепта для поиска"),
    db: Session = Depends(database.get_db),
) -> schemas.Recipe:
    """
    Получает рецепт по ID. Увеличивает счетчик просмотров
    каждый раз при обращении к рецепту.

    - **recipe_id**: ID рецепта, который нужно найти
    """
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    try:
        recipe.views += 1  # Увеличение счетчика просмотров
        db.commit()
        db.refresh(recipe)
    except BaseException:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Не удалось обновить счетчик просмотров"
        )
    return recipe


@router.post(
    "/recipes",
    response_model=schemas.Recipe,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый рецепт",
    description="Создаёт новый рецепт и сохраняет его в базе данных.",
)
def create_recipe(
    recipe: schemas.RecipeCreate, db: Session = Depends(database.get_db)
) -> schemas.Recipe:
    db_recipe = models.Recipe(
        title=recipe.title,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.delete(
    "/recipes/{recipe_id}",
    summary="Удалить рецепт",
    description="Удаляет рецепт по его ID из базы данных.",
)
def delete_recipe(
    recipe_id: int = Path(..., description="ID рецепта для удаления"),
    db: Session = Depends(database.get_db),
) -> Dict[str, str]:
    """
    Удаляет рецепт по ID.

    - **recipe_id**: ID рецепта, который нужно удалить
    """
    recipe = crud.get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    crud.delete_recipe(db, recipe_id)
    return {"detail": "Рецепт удален"}


@router.put(
    "/recipes/{recipe_id}",
    response_model=schemas.Recipe,
    summary="Обновить рецепт",
    description="Обновляет существующий рецепт по его ID.",
)
async def update_recipe(
    recipe_data: schemas.RecipeCreate,
    recipe_id: int = Path(..., description="ID рецепта для обновления"),
    db: Session = Depends(database.get_db),
) -> schemas.Recipe:
    """
    Обновляет существующий рецепт по ID на основе
    предоставленных данных.

    - **recipe_id**: ID рецепта, который нужно обновить
    - **title**: Новое название рецепта
    - **cooking_time**: Новое время приготовления
    - **ingredients**: Новые ингредиенты
    - **description**: Новое описание процесса приготовления
    """
    # Получаем рецепт из базы данных по ID
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    # Если рецепт не найден, возвращаем ошибку 404
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    # Обновляем атрибуты рецепта
    recipe.title = recipe_data.title
    recipe.cooking_time = recipe_data.cooking_time
    recipe.ingredients = recipe_data.ingredients
    recipe.description = recipe_data.description
    # Сохраняем изменения в базе данных
    db.commit()
    db.refresh(recipe)
    # Возвращаем обновленный рецепт
    return recipe
