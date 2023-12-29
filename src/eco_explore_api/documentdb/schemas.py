from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from pydantic_extra_types import PhoneNumber


class EquipoNecesario(BaseModel):
    Nombre: str
    Cantidad: int = 0


class PuntosInteres(BaseModel):
    Lon: float
    Lat: float
    UrlMedia: Optional(List[str])


class Reseña(BaseModel):
    Evaluacion: int
    Comentario: str


class Usuarios(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber


class Bitacora(BaseModel):
    Nombre: str
    Publica: bool
    Descripcion: str
    Activad: str
    Dificultad: int
    EquipoNecesario: Optional(List[EquipoNecesario])
    PuntosInteres: List[PuntosInteres()]
    Comentarios: Optional(List[Reseña()])


class Exploraciones(BaseModel):
    FechaAgendata: datetime
    Guia: Usuarios()
    Exploradores: List[Usuarios()]
    Ruta: Bitacora()
    Precio: float
