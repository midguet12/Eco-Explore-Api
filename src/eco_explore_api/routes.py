from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from eco_explore_api.schemas.responses import HealthCheckResponse, VersionResponse
import eco_explore_api.schemas.response_constants as rcodes

app = FastAPI()


@app.get("/health")
async def health():
    response = HealthCheckResponse(message="Is Health")
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
