from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL='mysql+aiomysql://root:123456@mysql:3306/anzhai_memo?charset=utf8mb4'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_database():
    return Base.metadata.create_all(bind=engine)


