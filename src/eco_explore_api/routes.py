import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from eco_explore_api.schemas.responses import (
    HealthCheckResponse,
    VersionResponse,
    EquipoNecesarioResponse,
    PuntosInteresResponse,
    ResenaResponse,
    UsuariosResponse,
    BitacoraResponse,
    ExploracionesResponse,
    StatusResponse,
)
from eco_explore_api.schemas import (
    response_constants as rcodes,
    errors,
)
import eco_explore_api.config as cf
import eco_explore_api.documentdb.document_operations as dc
import eco_explore_api.documentdb.schemas as sh
from pydantic import ValidationError

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


@app.post(
    "/signin",
    response_model=StatusResponse,
    tags=["Usuarios"],
)
async def sign_in(json_data: dict):
    try:
        # json_data = json.load(json_data)
        contenido = sh.Usuarios(**json_data)
        if dc.create_user(contenido):
            respuesta = StatusResponse(ok=True, detail="usuario Creado")
            return JSONResponse(
                status_code=rcodes.OK, content=jsonable_encoder(respuesta.model_dump())
            )
        else:
            res = StatusResponse(ok=False, detail="El usuario ya existe")
            return JSONResponse(
                status_code=rcodes.CONFLICT,
                content=jsonable_encoder(res.model_dump()),
            )
    except ValidationError as exc:
        error = errors.Error(error=str(exc.errors()[0]), detail=None)
        return JSONResponse(
            status_code=rcodes.BAD_REQUEST, content=jsonable_encoder(error.model_dump())
        )

@app.get(
    "/get_route",
    response_model=StatusResponse,
    tags=["Rutas"],
)
async def get_route(json_data: dict):
    try:
        contenido = sh.Bitacora(**json_data)
        route_object = dc.get_route(contenido)

        if route_object:
            respuesta = StatusResponse(ok=True, detail="Ruta encontrada")
            return JSONResponse(
                status_code=rcodes.OK,
                content=jsonable_encoder(respuesta.model_dump()),
            )
        else:
            res = StatusResponse(ok=False, detail="Ruta no encontrada")
            return JSONResponse(
                status_code=rcodes.NOT_FOUND,
                content=jsonable_encoder(res.model_dump()),
            )
    except ValidationError as exc:
        error = errors.Error(error=str(exc.errors()[0]), detail=None)
        return JSONResponse(
            status_code=rcodes.BAD_REQUEST,
            content=jsonable_encoder(error.model_dump()),
        )
    

class ExplorationUserResponse(BaseModel):
    active_bitacoras_count: int
    total_bitacoras_count: int
    explorations_count: int


@app.get(
    "/get_explorations_user",
    response_model=ExplorationUserResponse,
    tags=["Usuarios"],
)
async def get_explorations_user(json_data: dict):
    try:
        contenido = sh.Usuarios(**json_data)
        active_bitacoras_count, total_bitacoras_count, explorations_count = dc.get_ExplorationUser(contenido)

        return ExplorationUserResponse(
            active_bitacoras_count=active_bitacoras_count,
            total_bitacoras_count=total_bitacoras_count,
            explorations_count=explorations_count,
        )

    except ValidationError as exc:
        error = {"detail": str(exc.errors()[0])}
        raise HTTPException(status_code=rcodes.BAD_REQUEST, detail=error)

    except Exception as e:
        error = {"detail": str(e)}
        raise HTTPException(status_code=rcodes.INTERNAL_SERVER_ERROR, detail=error)
