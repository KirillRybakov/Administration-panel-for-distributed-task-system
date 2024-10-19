from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Настройка подключения к базе данных
DATABASE_URL = "postgresql+asyncpg://petdb:11111111@postgres:5432/petdb"

# Создаём асинхронный движок для работы с БД
engine = create_async_engine(DATABASE_URL, echo = True)

# Создаём  фабрику сессий для асинхронной работы
async_session = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False
)

Base = declarative_base()

# Асинхронная зависимость для сессий
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


