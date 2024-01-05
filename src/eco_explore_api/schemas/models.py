from pydantic import Field
from typing import Optional
import eco_explore_api.documentdb.schemas as models


class BitacoraModel(models.Bitacora):
    id: Optional[str] = Field(alias="_id")


class UsuariosModel(models.Usuarios):
    id: Optional[str] = Field(alias="_id")
    # exclude = ["Clave"]


class ExploracionesModel(models.Exploraciones):
    id: Optional[str] = Field(alias="_id")


class Reseña(models.Reseña):
    id: Optional[str] = Field(alias="_id")
