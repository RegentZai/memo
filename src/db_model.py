from sqlalchemy import Column, String, Integer
from .db import Base

class InfoDB(Base):
    __tablename__ = "info"

    id           = Column(Integer,       primary_key=True, autoincrement=True)
    name         = Column(String(64),    nullable=True)
    memorandum   = Column(String(64),    nullable=True)

    def __init__(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
