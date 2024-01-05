from pydantic import BaseModel
from typing import List, Optional


class ComentaryRequest(BaseModel):
    Comentarios: Optional[List[str]]
