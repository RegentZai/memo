"""数据库实例化"""
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.constants.config import settings

# 初始化数据库
class Base(AsyncAttrs, DeclarativeBase):
    pass

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(bind=engine)

# 获取数据库
async def get_db():
    async with SessionLocal() as session:
        yield session
