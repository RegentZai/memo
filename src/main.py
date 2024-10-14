from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware

from .db import init_database
from .db_model import InfoDB
from .api_models import InfoAPI
from .find import add, remove, update, find, find_id

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)

@app.on_event("startup")
async def startup():
    # 初始化数据库
    init_database()

@app.get('/ping')
def pong():
    """healthcheck"""
    return Response(content='pong')

@app.post('/add')
async def addinfo(info: InfoAPI):
    addinfo = InfoDB(
        name=info.name,
        memorandum=info.memorandum,
    )
    try:
        add(addinfo)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/find')
async def findinfo(name: str):
    info = find(name)
    if info is not None:
        return info
    else:
        return 'nomessage'

@app.get('/remove')
async def rminfo(id: int):
    info = find_id(name)
    if info is not None:
        remove(info)
    else:
        return 'nomessage'

@app.post('/update')
async def updateinfo(info: InfoAPI):
    updateinfo = InfoDB(
        name=info.name,
        memorandum=info.memorandum,
    )
    try:
        update(updateinfo)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))