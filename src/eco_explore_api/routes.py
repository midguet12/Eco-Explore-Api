from fastapi import Depends, FastAPI, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
#from eco_explore_api.auth.utils import VerifyToken
from datetime import datetime
from eco_explore_api.schemas.responses import HealthCheckResponse, VersionResponse
import eco_explore_api.schemas.response_constants as rcodes
import eco_explore_api.config as cf


token_auth_scheme = HTTPBearer()

app = FastAPI()
#auth = VerifyToken()


@app.get("/health", response_model=HealthCheckResponse())
async def health():
    response = HealthCheckResponse(message="Hola {}".format(cf.AUTH0_API_AUDIENCE))
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


#@app.get("/api/private")
#def private(auth_result: str = Security(auth.verify)):
#    """A valid access token is required to access this route"""
#    return auth_result
