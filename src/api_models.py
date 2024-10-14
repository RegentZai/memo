from __future__ import annotations
from pydantic import BaseModel as PydanticBaseModel
from typing import Optional
import datetime

#配置pydantic允许接受任意类型的数据作为输入
class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True

class InfoAPI(BaseModel):
    name:       str                         = None  #留言人
    memorandum: Optional[str]               = None  #备忘录

