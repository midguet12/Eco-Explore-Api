from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List
from eco_explore_api.schemas.responses import (
    HealthCheckResponse,
    VersionResponse,
    EquipoNecesarioResponse,
    PuntosInteresResponse,
    ResenaResponse,
    UsuariosResponse,
    BitacoraResponse,
    ExploracionesResponse,
)
import eco_explore_api.schemas.response_constants as rcodes
import eco_explore_api.config as cf

app = FastAPI()


@app.get("/health", response_model=HealthCheckResponse())
async def health(saludo):
    response = HealthCheckResponse(message="Adios {}".format(saludo))
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(response))


@app.get("/status")
async def statue():
    time = datetime.now()
    return JSONResponse(
        status_code=rcodes.OK,
        content=jsonable_encoder(
            VersionResponse(version=1.0, detail=(HealthCheckResponse(time=time)))
        ),
    )


@app.get("/usuarios", response_model=List[UsuariosResponse], tags=["Usuarios"])
async def get_usuarios():
    usuarios = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(usuarios))


@app.get(
    "/puntos_interes/",
    response_model=List[PuntosInteresResponse],
    tags=["Puntos de Interés"],
)
async def get_puntos_interes():
    puntos_interes = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(puntos_interes))


@app.get("/resenas/", response_model=List[ResenaResponse], tags=["Reseñas"])
async def get_resenas():
    resenas = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(resenas))


@app.get(
    "/equipos_necesarios/",
    response_model=List[EquipoNecesarioResponse],
    tags=["Equipos Necesarios"],
)
async def get_equipos_necesarios():
    equipos = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(equipos))


@app.get("/bitacoras/", response_model=List[BitacoraResponse], tags=["Bitácoras"])
async def get_bitacoras():
    bitacoras = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(bitacoras))


@app.get(
    "/exploraciones/",
    response_model=List[ExploracionesResponse],
    tags=["Exploraciones"],
)
async def get_exploraciones():
    exploraciones = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(exploraciones))
