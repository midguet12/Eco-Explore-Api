from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import eco_explore_api.documentdb.schemas as models
from pydantic_extra_types.phone_numbers import PhoneNumber


class BitacoraModel(models.Bitacora):
    id: Optional[str] = Field(alias="_id")


class UsuariosModelChecker(BaseModel):
    Nombre: str
    ApellidoPaterno: str
    ApellidoMaterno: str
    Email: EmailStr
    UrlImagen: str
    PerfilPublico: bool
    Guia: bool
    Telefono: PhoneNumber
    Bitacoras: Optional[List[str]]
    # exclude = ["Clave"]


class UsuariosModel(UsuariosModelChecker):
    id: Optional[str] = Field(alias="_id")


class ExploracionesModel(models.Exploraciones):
    id: Optional[str] = Field(alias="_id")


class Reseña(models.Reseña):
    id: Optional[str] = Field(alias="_id")
