from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List, Dict
from .. import crud, schemas, models, database


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
    популярности (по количеству просмотров) и времени приготовления
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
    summary="Создать новый рецепт",
    description="Создаёт новый рецепт и сохраняет его в базе данных.",
)
def create_recipe(
    recipe: schemas.RecipeCreate, db: Session = Depends(database.get_db)
) -> schemas.Recipe:
    """
    Создаёт новый рецепт на основе предоставленных данных.

    - **title**: Название рецепта
    - **cooking_time**: Время приготовления в минутах
    - **ingredients**: Ингредиенты рецепта
    - **description**: Описание процесса приготовления
    """
    db_recipe = models.Recipe(**recipe.model_dump())
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
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    for field, value in recipe_data.model_dump().items():
        setattr(recipe, field, value)
    db.commit()
    db.refresh(recipe)
    return recipe
