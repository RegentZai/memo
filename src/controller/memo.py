from fastapi import APIRouter, Body, Depends, Path, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants.config import limiter
from src.constants.constant import Error, ErrorMes
from src.model import req, resp
from src.service import memo_util
from src.storage.db import get_db

memoRouter = APIRouter(prefix="/memo", tags=["memo"])

@memoRouter.get("/ping")
def pong():
    """healthcheck"""
    return Response(content="pong")


@memoRouter.get("/", response_model=resp.MemoResponse)
@limiter.limit("1/seconds")
async def Get_all(request: Request, response: Response, session: AsyncSession = Depends(get_db)):
    """获取备忘录"""
    try:
        memos_row = await memo_util.find_memo_all(session)
    except Exception:
        raise resp.ErrResponse(Error.DbErr, "fail to get memo:Unkown Error Happened", status.HTTP_500_INTERNAL_SERVER_ERROR)


    memo_list = []
    for memo_row in memos_row:
        memo = resp.MemoSchema.model_validate(memo_row._asdict())
        memo_list.append(memo)

    return resp.MemoResponse(memos=memo_list)


@memoRouter.post("/")
@limiter.limit("1/seconds")
async def Create_memo(request: Request, response: Response, create_body: req.CreateMemoRequest = Body(), sess: AsyncSession = Depends(get_db)):
    """创建备忘录"""

    try:
        memo = await memo_util.create_memo(create_body, sess)
    except Exception:
        raise resp.ErrResponse(Error.DbErr, "fail to create memo:Unkown Error Happened", status.HTTP_500_INTERNAL_SERVER_ERROR)
    return resp.APIResponse(errCode=Error.NoError)


@memoRouter.patch("/{id}")
@limiter.limit("1/seconds")
async def Update_memo(request: Request, response: Response, id: int = Path(), update_body: req.UpdateMemoRequest = Body(), sess: AsyncSession = Depends(get_db)):
    """更新备忘录"""

    try:
        memo_row = await memo_util.find_memo_by_id(id, sess)
    except Exception:
        raise resp.ErrResponse(Error.DbErr, "fail to get memo:Unkown Error Happened", status.HTTP_500_INTERNAL_SERVER_ERROR)

    if memo_row is None:
        raise resp.ErrResponse(Error.MemoNotFound, ErrorMes[Error.MemoNotFound], status.HTTP_404_NOT_FOUND)

    try:
        memo_new = await memo_util.update_memo(memo_row.id, update_body.model_dump(exclude_none=True), sess)
    except Exception:
        raise resp.ErrResponse(Error.DbErr, "fail to update memo:Unkown Error Happened", status.HTTP_500_INTERNAL_SERVER_ERROR)

    return resp.APIResponse(errCode=Error.NoError)


@memoRouter.delete("/{id}")
@limiter.limit("1/seconds")
async def Delete_memo(request: Request, response: Response, id: int = Path(), sess: AsyncSession = Depends(get_db)):
    """删除备忘录"""
    try:
        memo_row = await memo_util.find_memo_by_id(id, sess)
    except Exception:
        raise resp.ErrResponse(Error.DbErr, "fail to get memo:Unkown Error Happened", status.HTTP_500_INTERNAL_SERVER_ERROR)
    if memo_row is None:
        raise resp.ErrResponse(Error.NoMsg, ErrorMes[Error.NoMsg], status.HTTP_404_NOT_FOUND)

    try:
        await memo_util.delete_memo(id, sess)
    except Exception:
        raise resp.ErrResponse(Error.DbErr, "fail to delete product:Unkown Error Happened", status.HTTP_500_INTERNAL_SERVER_ERROR)

    return resp.APIResponse(errCode=Error.NoError)
