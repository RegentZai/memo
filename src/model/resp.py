import datetime

from pydantic import BaseModel

from src.constants.constant import Error, ErrorMes

# 通用返回
class APIResponse(BaseModel):
    errCode: int = Error.NoError
    message: str = ErrorMes[Error.NoError]


# 异常错误，返回错误信息（非20x响应码）
class ErrResponse(Exception):
    def __init__(self, errCode: int, message: str, code: int):
        self.errCode = errCode
        self.message = message
        self.status_code = code


class MemoSchema(BaseModel):
    id:          int               # id
    name:        str               # 昵称
    category:    str               # 类别
    content:     str               # 文本



class MemoResponse(APIResponse):
    memos: list[MemoSchema] = []  # 列表

