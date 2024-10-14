from typing import Union
from .db import SessionLocal
from .db_model import InfoDB

def find(name: str) -> Union[InfoDB, None]:
    """查找数据库"""
    with SessionLocal() as sess:
        return sess.query(InfoDB).filter_by(name=name).all()

def find_id(id: int) -> Union[InfoDB, None]:
    """检查数据库"""
    with SessionLocal() as sess:
        return sess.query(InfoDB).filter_by(id=id).first()

def update(item):
    """更新数据库"""
    with SessionLocal() as sess:
        merged_item = sess.merge(item)
        sess.commit()
        sess.refresh(merged_item)

def add(item):
    """添加到数据库"""
    with SessionLocal() as sess:
        sess.add(item)
        sess.commit()
        sess.refresh(item)
    return item

def remove(item):
    """从数据库中删除"""
    with SessionLocal() as sess:
        sess.delete(item)
        sess.commit()
