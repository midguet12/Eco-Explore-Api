from datetime import datetime
from typing import List, Optional, Annotated
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class EquipoNecesario(BaseModel):
    Nombre: str
    Cantidad: int = 0


class PuntosInteres(BaseModel):
    Lon: float
    Lat: float
    UrlMedia: Optional[str]


class Reseña(BaseModel):
    Evaluacion: int
    Comentario: str


class Bitacora(BaseModel):
    Nombre: str
    Publica: bool
    Descripcion: str
    Actividad: str
    Dificultad: str
    EquipoNecesario: Optional[List[EquipoNecesario]]
    PuntosInteres: List[PuntosInteres]
    Comentarios: Optional[List[str]]
    Puntuacion: float


class ModBitacora(BaseModel):
    Nombre: str
    Publica: bool
    Descripcion: str
    Actividad: str
    Dificultad: str


class Usuarios(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Clave: Annotated[str, Field(exclude=True)]
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber
    Bitacoras: Optional[List[str]]

class ModUsuarios(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber


class UsuariosModelAuth(Usuarios):
    id: Optional[str] = Field(alias="_id")


class Exploraciones(BaseModel):
    FechaAgendada: int
    Guia: str
    Exploradores: List[str]
    Ruta: str
    Precio: float
