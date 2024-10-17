from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from sqlalchemy import update

from src.model.db_model import Memorandum
from src.model.req import CreateMemoSchema


async def find_memo_all(sess: AsyncSession) -> list[Memorandum]:
    """查找所有备忘录"""
    result = await sess.execute(text("select * from memorandums"))
    return result.all()


async def find_memo_by_id(id: int, sess: AsyncSession) -> Memorandum:
    """通过id查找"""
    return await sess.get(Memorandum, id)


async def find_memo_by_name(name: str, sess: AsyncSession) -> Memorandum:
    """通过name查找"""
    result = await sess.execute(text("select * from memorandums where name = :name"), {"name": name})
    return result.all()


async def find_memo_by_category(category: str, sess: AsyncSession) -> Memorandum:
    """通过category查找"""
    result = await sess.execute(text("select * from memorandums where category = :category"), {"category": category})
    return result.all()


async def create_memo(memo: CreateMemoSchema, sess: AsyncSession) -> Memorandum:
    """创建新的备忘录"""
    db_product = Memorandum(memo.model_dump())
    sess.add(db_product)
    await sess.commit()
    await sess.refresh(db_product)
    return db_product


async def update_memo(id: int, update_field: dict, sess: AsyncSession) -> Memorandum:
    """更新备忘录"""
    memo_new = await find_memo_by_id(id, sess)
    for key, value in update_field.items():
        setattr(memo_new, key, value)
    await sess.commit()
    await sess.refresh(memo_new)
    return memo_new


async def delete_memo(id: int, sess: AsyncSession):
    """删除备忘录"""
    memo = await find_memo_by_id(id, sess)
    await sess.delete(memo)
    await sess.commit()


async def update_memo_surplus_quantity(id, new_surplus_quantity, session: AsyncSession):
    """更新备忘录"""
    update_stmt = (
        update(Memorandum)
        .where(Memorandum.memo_id == id)
        .values({Memorandum.surplus_quantity: new_surplus_quantity})
    )
    await session.execute(update_stmt)
    await session.commit()
