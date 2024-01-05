from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from fastapi import UploadFile
from eco_explore_api.schemas import models
from eco_explore_api.documentdb.schemas import Reseña
from pydantic_extra_types.phone_numbers import PhoneNumber


class RequestFiles(BaseModel):
    body: dict
    object: UploadFile


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


class UsuariosResponse(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber


class ExploracionesResponse(BaseModel):
    Agenda: Optional[List[models.ExploracionesModel]]


class StatusResponse(BaseModel):
    ok: bool
    detail: Optional[str]


class CreatedObjectResponse(StatusResponse):
    id: Optional[str]


class BestRoutesResponse(BaseModel):
    Rutas: Optional[List[models.BitacoraModel]]


class UsersResponse(BaseModel):
    Usuarios: Optional[List[models.UsuariosModel]]


class UserRoutesResponse(BaseModel):
    Guadadas: Optional[BestRoutesResponse]
    Publicas: Optional[BestRoutesResponse]


class GoogleStorageResponse(BaseModel):
    bucket: str
    blob_path: str
    file_name: str
    file_path: str
    file_size: str
    content_type: str


class ComentaryResponse(BaseModel):
    Comentarios: Optional[List[Reseña]]
