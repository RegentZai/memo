"""一些常量"""

from enum import IntEnum, auto


class Error(IntEnum):
    NoError = 0
    DbErr = auto()  # 1
    NoMsg = auto()  # 2
    MemoNotFound = auto() # 3




# 将上述的error枚举转换为字典
ErrorMes = {
    # NoError: "无错误"
    Error.NoError: "No Error",
    # DbErr: "数据库调取错误"
    Error.DbErr: "Database Error",
    # NoMsg："目标信息不存在"
    Error.NoMsg: "No Message",
    # MemoNotFound: "目标备忘录不存在"
    Error.MemoNotFound: "Memorandum Not Found"


}
