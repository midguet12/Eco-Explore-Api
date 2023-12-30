from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class EquipoNecesario(BaseModel):
    Nombre: str
    Cantidad: int = 0


class PuntosInteres(BaseModel):
    Lon: float
    Lat: float
    UrlMedia: Optional[List[str]]


class Reseña(BaseModel):
    Evaluacion: int
    Comentario: str


class Bitacora(BaseModel):
    Nombre: str
    Publica: bool
    Descripcion: str
    Activad: str
    Dificultad: int
    EquipoNecesario: Optional[List[EquipoNecesario]]
    PuntosInteres: List[PuntosInteres]
    Comentarios: Optional[List[str]]
    Puntuacion: float


class Usuarios(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber
    Bitacoras: Optional[List[str]]


class Exploraciones(BaseModel):
    FechaAgendata: datetime
    Guia: str
    Exploradores: List[str]
    Ruta: str
    Precio: float
