"""数据库实例化"""

from sqlalchemy import Column, DateTime, Integer, String, Text

from src.storage.db import Base


class Memorandum(Base):
    __tablename__ = "memorandums"

    id          = Column(Integer, primary_key=True, autoincrement=True, index=True)
    # 昵称
    name        = Column(String(64), nullable=False, index=True)
    # 类别
    category    = Column(String(64), nullable=False, index=True)
    # 文本
    content     = Column(Text,       nullable=False)

    def __init__(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

