from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from pydantic_extra_types.phone_numbers import PhoneNumber


class HealthCheckResponse(BaseModel):
    message: Optional[str] = ""
    time: Optional[datetime] = datetime.now()


class VersionResponse(BaseModel):
    version: float
    detail: HealthCheckResponse


class EquipoNecesarioResponse(BaseModel):
    Nombre: str
    Cantidad: int = 0


class PuntosInteresResponse(BaseModel):
    Lon: float
    Lat: float
    UrlMedia: Optional[List[str]]


class ResenaResponse(BaseModel):
    Evaluacion: int
    Comentario: str


class UsuariosResponse(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber


class BitacoraResponse(BaseModel):
    Nombre: str
    Descripcion: str
    Dificultad: int
    EquipoNecesario: Optional[List[EquipoNecesarioResponse]]
    PuntosInteres: List[PuntosInteresResponse]
    Comentarios: Optional[List[ResenaResponse]]


class ExploracionesResponse(BaseModel):
    FechaAgendata: datetime
    Guia: UsuariosResponse
    Exploradores: List[UsuariosResponse]
    Ruta: BitacoraResponse
    Precio: float
