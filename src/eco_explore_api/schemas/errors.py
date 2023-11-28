from typing import List, Optional
from pydantic import BaseModel


class Detail(BaseModel):
    title: Optional(str | int)
    desc: int | str | List[str] | List[int]


class Error(BaseModel):
    error: str
    detail: Optional(List[Detail])
