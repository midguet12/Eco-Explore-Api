import bson
from pymongo import ASCENDING
import eco_explore_api.config as cf
from eco_explore_api.schemas import errors
import eco_explore_api.documentdb.schemas as schemas
import eco_explore_api.constants.delimitations as limits
from eco_explore_api.documentdb.document import Collections
import eco_explore_api.constants.response_constants as rcodes
from eco_explore_api.schemas.responses import (
    BestRoutesResponse,
    UserRoutesResponse,
    ExplorationScheduleResponse,
    ResenaResponse,
)


def serialice_id(uid: str):
    return bson.ObjectId(uid)


def valid_user_id(user_id: str):
    try:
        user_id = serialice_id(user_id)
        return True
    except Exception:
        return False


def user_exist(user_id: str):
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    usr_serach = {"_id": user_id}
    ans = cls.find_one(filter=usr_serach)
    return bool(ans)


def create_user(Usuario: schemas.Usuarios):
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    ans = cls.find_one({"Email": Usuario.Email})
    if not ans:
        ans = cls.insert_one(Usuario.model_dump())
        return ans.acknowledged
    return False


def find_best_routes(acivity: str):
    acivity = acivity.strip("").lower()
    response = BestRoutesResponse(Rutas=[])
    if acivity not in limits.ACTIVITIES:
        return [
            rcodes.BAD_REQUEST,
            errors.Error(
                error="Actividad no encontrada", detail=",".join(limits.ACTIVITIES)
            ),
        ]
    cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
    search_criteria = {"Actividad": acivity}
    ans = list(cls.find(filter=search_criteria).sort("Puntuacion", ASCENDING).limit(7))
    if len(ans):
        for bitacora in ans:
            try:
                current = schemas.Bitacora(**bitacora)
                response.Rutas.append(current)
            except Exception as e:
                return [
                    rcodes.NOT_FOUND,
                    errors.Error(error="Error al Obtener bitacoras", detail=str(e)),
                ]
            return [rcodes.ok, response]
    else:
        return [rcodes.NOT_FOUND, response]


def exploration_details(user_id: str):
    response = UserRoutesResponse(
        Guadadas=BestRoutesResponse(Rutas=[]), Publicas=BestRoutesResponse(Rutas=[])
    )
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(user_id):
        errorResponse.error = "user id invalido"
        return [rcodes.BAD_REQUEST, errorResponse]

    user_id = serialice_id(user_id)
    if user_exist(user_id):
        bitacoras = []
        cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
        for elements in ans["Bitacoras"]:
            bit = cls.find_one(filter={"_id": elements})
            if bit:
                for id in bit["Comentarios"]:
                    id = str(id)
                try:
                    bit.pop("_id", None)
                    bitacoras.append(schemas.Bitacora(**bit))
                except Exception as e:
                    errorResponse.error = "Error al recuperar las bitacoras"
                    errorResponse.detail = str(e)
                    return [rcodes.CONFLICT, errorResponse]

        for element in bitacoras:
            if element.Publica:
                response.Publicas.Rutas.append(element)
            else:
                response.Guadadas.Rutas.append(element)

        return [rcodes.OK, response]
    else:
        errorResponse.error = "El usuario no existe"
        return [rcodes.NOT_FOUND, errorResponse]


def exploration_schedule(user_id: str):
    response = ExplorationScheduleResponse(Agenda=None)
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(user_id):
        errorResponse.error = "user id invalido"
        return [rcodes.BAD_REQUEST, errorResponse]
    user_id = serialice_id(user_id)
    # if user_exist(user_id):


def update_user(user_id: str, updated_user: schemas.Usuarios):
    cls = Collections().get_collection(cf.USERS_COLLECTION)

    user_id = serialice_id(user_id)

    if user_exist(user_id):
        try:
            cls.update_one({"_id": user_id}, {"$set": updated_user.model_dump()})
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            return False
    else:
        return False


def add_review_to_bitacora(bitacora_id: str, user_id: str, resena: schemas.Reseña):
    cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
    col = Collections().get_collection(cf.COMENTARY_COLLECTION)

    bitacora_id = serialice_id(bitacora_id)

    user_id = serialice_id(user_id)

    if user_exist(user_id):
        try:
            resena_id = col.insert_one(resena.model_dump()).inserted_id

            cls.update_one({"_id": bitacora_id}, {"$push": {"Comentarios": resena_id}})

            bitacora = cls.find_one({"_id": bitacora_id})
            comentarios_ids = bitacora.get("Comentarios", [])

            puntuaciones = []
            for comentario_id in comentarios_ids:
                comentario = col.find_one({"_id": comentario_id})
                puntuaciones.append(comentario.get("Evaluacion", 0))

            if puntuaciones:
                promedio = round(sum(puntuaciones) / len(puntuaciones), 1)

                cls.update_one({"_id": bitacora_id}, {"$set": {"Puntuacion": promedio}})

            respuesta = ResenaResponse(
                Evaluacion=resena.Evaluacion, Comentario=resena.Comentario
            )
            return rcodes.OK, respuesta
        except Exception as e:
            print(f"Error al agregar reseña a la bitácora: {e}")
            errorResponse = errors.Error(error="Error al agregar reseña", detail=str(e))
            return rcodes.INTERNAL_SERVER_ERROR, errorResponse
    else:
        errorResponse = errors.Error(error="El usuario no existe", detail=None)
        return rcodes.NOT_FOUND, errorResponse
