from sqlalchemy.orm import Session
from typing import Generator
from .config import Base, engine, SessionLocal


def init_db() -> None:
    """
    Инициализирует базу данных, создавая все таблицы, определенные в модели.

    :return: None
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Получает сессию базы данных, управляя ее жизненным циклом.
    Используйте эту функцию в качестве зависимости FastAPI для автоматического
    управления подключением к базе данных.

    :yield: Сессия базы данных
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
