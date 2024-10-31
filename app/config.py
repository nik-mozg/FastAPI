from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL для базы данных SQLite
DATABASE_URL: str = "sqlite:///./culinary_db.sqlite"

# Создаем движок для подключения к базе данных с отключенной проверкой потока
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Конфигурируем сессию для взаимодействия с базой данных
SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Базовый класс, который будет использоваться для всех моделей,
# определяющих структуру базы данных
Base = declarative_base()
