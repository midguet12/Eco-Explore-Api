import json
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import List, Annotated
from eco_explore_api.constants import response_constants as rcodes
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
    BestRoutesResponse,
    UserRoutesResponse,
    CreatedObjectResponse,
)
from eco_explore_api.schemas import errors, models
import eco_explore_api.config as cf
import eco_explore_api.documentdb.document_operations as dc
import eco_explore_api.documentdb.schemas as sh
from pydantic import ValidationError
from eco_explore_api.storage.google_storage import gstorage

app = FastAPI()


@app.get("/health", response_model=HealthCheckResponse)
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
    "/puntos/interes",
    response_model=List[PuntosInteresResponse],
    tags=["Puntos de Interés"],
)
async def get_puntos_interes():
    puntos_interes = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(puntos_interes))


@app.get("/resenas", response_model=List[ResenaResponse], tags=["Reseñas"])
async def get_resenas():
    resenas = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(resenas))


@app.get(
    "/equipos/necesarios",
    response_model=List[EquipoNecesarioResponse],
    tags=["Equipos Necesarios"],
)
async def get_equipos_necesarios():
    equipos = []
    return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(equipos))


@app.get(
    "/bitacora/{bitacora_id}", response_model=models.BitacoraModel, tags=["Bitácoras"]
)
async def get_bitacoras(bitacora_id: str):
    code, response = dc.get_logbook(bitacora_id)
    return JSONResponse(
        status_code=code, content=jsonable_encoder(response.model_dump())
    )


@app.post(
    "/bitacoras/crear/{user_id}",
    response_model=CreatedObjectResponse,
    tags=["Bitácoras"],
)
async def create_bitacora(user_id: str, body: dict):
    code, response = dc.create_logbook(user_id, body)
    return JSONResponse(
        status_code=code, content=jsonable_encoder(response.model_dump())
    )


@app.put(
    "/bitacoras/agregar",
    response_model=StatusResponse,
    tags=["Bitácoras"],
)
async def add_pov(
    user_id: str,
    bitacora_id: str,
    coordinates: Annotated[str, Form()],
    file: Annotated[UploadFile, File()],
):
    try:
        coordinates = json.loads(coordinates)
    except Exception as e:
        return JSONResponse(
            status_code=rcodes.BAD_REQUEST,
            content=jsonable_encoder(
                errors.Error(error="Data invalida", detail=str(e))
            ),
        )

    code, response = await dc.add_point_to_logbook(
        user_id, bitacora_id, coordinates, file
    )
    return JSONResponse(
        status_code=code, content=jsonable_encoder(response.model_dump())
    )


@app.get(
    "/exploraciones/{user_id}",
    response_model=ExploracionesResponse,
    tags=["Exploraciones"],
)
async def get_exploraciones(user_id: str):
    code, response = dc.exploration_schedule(user_id)
    return JSONResponse(
        status_code=code, content=jsonable_encoder(response.model_dump())
    )


@app.get(
    "/mejores/rutas/{activity}",
    response_model=BestRoutesResponse,
    tags=["Exploraciones"],
)
async def get_best_rotes(activity: str):
    code, response = dc.find_best_routes(activity)
    return JSONResponse(
        status_code=code, content=jsonable_encoder(response.model_dump())
    )


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
    "/exploraciones/detalles/{userid}",
    response_model=UserRoutesResponse,
    tags=["Exploraciones"],
)
async def exploration_details(userid: str):
    code, response = dc.exploration_details(userid)
    return JSONResponse(
        status_code=code, content=jsonable_encoder(response.model_dump())
    )


@app.post(
    "/bitacoras/subir/{id}",
    tags=["bitacoras"],
)
async def upload_to(id: str, file: UploadFile):
    storage = gstorage()
    try:
        response = await storage.upload_single_file(file)
        return JSONResponse(status_code=rcodes.OK, content=jsonable_encoder(response))
    except Exception as e:
        error = errors.Error(error="No fue posible subir el archivo", detail=str(e))
        return JSONResponse(
            status_code=rcodes.BAD_REQUEST,
            content=jsonable_encoder(error.model_dump()),
        )


@app.post("/files/{id1}/{id2}")
async def create_file(
    # file: Annotated[bytes, File()],
    id1: str,
    id2: str,
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, dict],
):
    token = json.loads(token)
    return {
        "id1": id1,
        "id2": id2,
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
