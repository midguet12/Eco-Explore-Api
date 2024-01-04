from pydantic import BaseModel
from typing import List, Optional


class ComentaryRequest(BaseModel):
    Comentarios_id: Optional[List[str]]
