from pydantic import BaseModel
import datetime

class DeleteMemoRequest(BaseModel):
    id: int

class CreateMemoRequest(BaseModel):
    name:     str
    category: str
    content:  str

class UpdateMemoRequest(BaseModel):
    name:     str
    category: str
    content:  str


class CreateMemoSchema(BaseModel):
    name:        str
    category:    str
    content:     str


class UpdateMemoSchema(BaseModel):
    name:        str
    category:    str
    content:     str
