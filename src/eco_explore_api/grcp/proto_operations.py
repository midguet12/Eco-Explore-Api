from eco_explore_api.grcp.client import GrpcServer
from eco_explore_api.schemas.responses import ComentaryResponse
import eco_explore_api.constants.response_constants as rcodes
from eco_explore_api.grcp.schemas import ComentaryRequest
from eco_explore_api.schemas.errors import Error


def get_comentary(comentary_ids: dict):
    errorResponse = Error(error="", detail=None)
    try:
        ComentaryRequest.model_validate(comentary_ids)
    except Exception as e:
        errorResponse.error = "Objeto Invalido"
        return [rcodes.BAD_REQUEST, errorResponse]

    user_data = ComentaryRequest(**comentary_ids)
    try:
        response = ComentaryResponse(Comentarios=[])
        cliente = GrpcServer()
        for id in user_data.Comentarios:
            ans = cliente.get_comentary(id)
            if ans:
                response.Comentarios.append(ans)
        return [rcodes.OK, response]
    except Exception as e:
        errorResponse.error = "No se pudieron recuperar los comentarios"
        errorResponse.detail = str(e)
        return [rcodes.CONFLICT, errorResponse]
