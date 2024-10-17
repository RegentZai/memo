"""启动函数"""

import logging
import logging.handlers
import os
import sys
import traceback
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

pythonpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, pythonpath)

from src.constants.config import corsConfig, limiter, settings
from src.controller import memo
from src.model.resp import ErrResponse
from src.storage.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """startup event"""
    # 初始化日志
    # 初始化数据库
    init_logger()
    await init_database()

    yield


app = FastAPI(lifespan=lifespan)

# 路由
app.include_router(memo.memoRouter)

# 自定义异常处理
@app.exception_handler(ErrResponse)
async def err_response_exception_handler(request: Request, exc: ErrResponse):
    if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        excMes = traceback.format_exc()
        endIndex = excMes.rfind("During handling of the above exception, another exception occurred:")
        errMes = excMes[:endIndex]
        errorlogger.error(errMes)
        print(errMes)
    if exc.status_code != status.HTTP_200_OK:
        errorlogger.info(exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"code": exc.errCode, "message": exc.message}),
    )


# 限流
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# 数据库初始化
async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



accesslogger = logging.getLogger("uvicorn.access")
errorlogger = logging.getLogger()


def init_logger():
    accesslogger = logging.getLogger("uvicorn.access")
    handler = logging.handlers.RotatingFileHandler(settings.ACCESS_LOG, mode="a", maxBytes=1024 * 1024, backupCount=10)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    accesslogger.addHandler(handler)
    handler2 = logging.handlers.RotatingFileHandler(settings.ERROR_LOG, mode="a", maxBytes=1024 * 1024, backupCount=10)
    handler2.setFormatter(logging.Formatter("%(asctime)s - %(name)s -%(levelname)s - %(message)s"))
    errorlogger.addHandler(handler2)


# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=corsConfig.ALLOWED_ORIGINS,  # 允许所有来源
    allow_credentials=corsConfig.ALLOWED_CREDENTIALS,
    allow_methods=corsConfig.ALLOWED_METHODS,  # 允许所有 HTTP 方法
    allow_headers=corsConfig.ALLOWED_HEADERS,  # 允许所有 HTTP 头部
)


# 测试接口
@app.get("/ping")
def pong():
    """healthcheck"""
    return Response(content="pong")
