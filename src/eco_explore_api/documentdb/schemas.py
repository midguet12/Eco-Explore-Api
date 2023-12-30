from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from pydantic_mongo import ObjectIdField
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
    Comentarios: Optional[List[ObjectIdField]]


class Usuarios(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber
    Bitacoras: Optional[List[ObjectIdField]]


class Exploraciones(BaseModel):
    FechaAgendata: datetime
    Guia: ObjectIdField
    Exploradores: List[ObjectIdField]
    Ruta: ObjectIdField
    Precio: float
