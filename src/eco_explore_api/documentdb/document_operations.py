import bson
from fastapi import UploadFile
import bson.json_util as json_util
from pymongo import DESCENDING
import eco_explore_api.config as cf
from eco_explore_api.schemas import errors
import eco_explore_api.documentdb.schemas as schemas
import eco_explore_api.schemas.models as models
import eco_explore_api.constants.delimitations as limits
from eco_explore_api.documentdb.document import Collections
import eco_explore_api.constants.response_constants as rcodes
from eco_explore_api.schemas.responses import (
    BestRoutesResponse,
    UserRoutesResponse,
    ExploracionesResponse,
    CreatedObjectResponse,
    StatusResponse,
    GoogleStorageResponse,
)
from eco_explore_api.storage.google_storage import gstorage


def serialice_id(uid: str):
    return bson.ObjectId(uid)


def valid_user_id(user_id: str):
    try:
        user_id = serialice_id(user_id)
        return True
    except Exception:
        return False


def transform_id_object(obj: dict):
    for element in obj:
        curr = obj[element]
        if isinstance(curr, list):
            curr = [str(x) for x in curr if bson.ObjectId.is_valid(x)]
            obj[element] = curr
        elif bson.ObjectId.is_valid(curr):
            obj[element] = str(curr)
    return obj


def user_exist(user_id: bson.ObjectId):
    if isinstance(user_id, str):
        user_id = serialice_id(user_id)
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


def get_logbook(id: str):
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(id):
        errorResponse.error = "El id de bitacora es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]
    search = {"_id": serialice_id(id)}
    cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
    ans = cls.find_one(filter=search)
    if ans:
        ans = transform_id_object(dict(ans))
        try:
            models.BitacoraModel.model_validate(ans)
        except Exception as e:
            errorResponse.error = "Ocurrio un error al recuperar la bitacora"
            errorResponse.detail = str(e)
            return [rcodes.CONFLICT, errorResponse]
        return [rcodes.OK, models.BitacoraModel(**ans)]
    else:
        errorResponse.error = "La bitacora no existe"
        return [rcodes.NOT_FOUND, errorResponse]


def find_best_routes(acivity: str):
    acivity = acivity.strip("").lower().capitalize()
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
    ans = list(cls.find(filter=search_criteria).sort("Puntuacion", DESCENDING).limit(7))
    if len(ans):
        for bitacora in ans:
            try:
                element = transform_id_object(bitacora)
                current = models.BitacoraModel(**element)
                response.Rutas.append(current)
            except Exception as e:
                return [
                    rcodes.NOT_FOUND,
                    errors.Error(error="Error al Obtener bitacoras", detail=str(e)),
                ]
        return [rcodes.OK, response]
    else:
        return [rcodes.NOT_FOUND, response]


def exploration_details(user_id: str):
    response = UserRoutesResponse(
        Guadadas=BestRoutesResponse(Rutas=[]), Publicas=BestRoutesResponse(Rutas=[])
    )
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(user_id):
        errorResponse.error = "El id del usuario es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]

    user_id = serialice_id(user_id)
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    usr_serach = {"_id": user_id}
    ans = cls.find_one(filter=usr_serach)
    if ans:
        bitacoras = []
        cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
        for elements in ans["Bitacoras"]:
            bit = cls.find_one(filter={"_id": elements})
            if bit:
                for id in bit["Comentarios"]:
                    id = str(id)
                try:
                    bitacoras.append(models.BitacoraModel(**transform_id_object(bit)))
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
    response = ExploracionesResponse(Agenda=[])
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(user_id):
        errorResponse.error = "El id del usuario es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]
    user_id = serialice_id(user_id)
    if user_exist(user_id):
        cls = Collections().get_collection(cf.EXPLORATION_COLLECTION)
        search_filter = {"Guia": user_id, "Exploradores": [user_id]}
        ans = list(cls.find(filter=search_filter))
        for element in ans:
            try:
                schedule = models.ExploracionesModel(**transform_id_object(element))
                response.Agenda.append(schedule)
            except Exception as e:
                errorResponse.error = "Recuperar Exploraciones"
                errorResponse.detail = str(e)
                return [rcodes.CONFLICT, errorResponse]
        return [rcodes.OK, response]
    else:
        errorResponse.error = "El usuario no existe"
        return [rcodes.NOT_FOUND, errorResponse]


def create_logbook(user_id: str, object: dict):
    response = CreatedObjectResponse(detail=None, id=None, ok=True)
    errorResponse = errors.Error(error="", detail=None)

    # check if user_id is valid:
    if not valid_user_id(user_id):
        errorResponse.error = "El id del usuario es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]
    # check if user exist
    user_id = serialice_id(user_id)
    if not user_exist(user_id):
        errorResponse.error = "El usuario no existe"
        return [rcodes.NOT_FOUND, errorResponse]

    try:
        schemas.Bitacora.model_validate(object)
    except Exception as e:
        errorResponse.error = "El Objeto no es valido"
        errorResponse.detail = str(e)
        return [rcodes.BAD_REQUEST, errorResponse]

    element = schemas.Bitacora(**object)
    element.Actividad = element.Actividad.lower().capitalize()
    element.Dificultad = element.Dificultad.lower().capitalize()
    if element.Actividad not in limits.ACTIVITIES:
        errorResponse.error = "Actividad Invalida"
        errorResponse.detail = ",".join(limits.ACTIVITIES)
        return [rcodes.BAD_REQUEST, errorResponse]

    if element.Dificultad not in limits.DIFICULTIES:
        errorResponse.error = "Dificultad Invalida"
        errorResponse.detail = ",".join(limits.DIFICULTIES)
        return [rcodes.BAD_REQUEST, errorResponse]
    try:
        cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
        ans = cls.insert_one(element.model_dump())
        if ans and ans.inserted_id:
            cls = Collections().get_collection(cf.USERS_COLLECTION)
            filter = {"_id": user_id}  # must be object Id
            update_obj = {
                "$push": {"Bitacoras": ans.inserted_id}
            }  # ans.inserted_id must be object id
            user = cls.update_one(filter=filter, update=update_obj, upsert=False)
            if user:
                response.detail = "bitacora creada"
                response.id = str(ans.inserted_id)
                return [rcodes.CREATED, response]
            else:
                errorResponse = "La bitacora no fue creada"
                return [rcodes.NOT_MODIFIED, errorResponse]

        else:
            errorResponse.error = "La bitacora no fue creada"
            return [rcodes.FORBIDDEN, errorResponse]
    except Exception as e:
        errorResponse.error = "La bitacora no fue creada"
        errorResponse.detail = str(e)
        return [rcodes.CONFLICT, errorResponse]


def its_user_logbook(user_id: str, bitacore_id):
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(user_id) or not valid_user_id(bitacore_id):
        errorResponse.error = "Uno de los ID no es valido"
        return [rcodes.BAD_REQUEST, errorResponse]

    cls = Collections().get_collection(cf.USERS_COLLECTION)
    search = {"_id": serialice_id(user_id)}
    ans = cls.find_one(filter=search)
    if ans:
        ans = models.UsuariosModel(**transform_id_object(dict(ans)))
        response = StatusResponse(
            ok=True, detail="{} pertenece a {}".format(str(bitacore_id), str(user_id))
        )
        if bitacore_id in ans.Bitacoras:
            return [rcodes.OK, response]
        else:
            response.ok = False
            response.detail = None
            return [rcodes.NOT_FOUND, response]
    else:
        errorResponse.error = "El usuario no existe"
        return [rcodes.NOT_FOUND, errorResponse]


async def add_point_to_logbook(
    user_id: str, bitacora_id: str, object: dict, image: UploadFile
):
    errorResponse = errors.Error(error="", detail="")
    if not valid_user_id(user_id):
        errorResponse.error = "El id del usuario es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]
    if not valid_user_id(bitacora_id):
        errorResponse.error = "El id de bitacora es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]

    codes, _ = its_user_logbook(user_id, bitacora_id)
    if codes == rcodes.NOT_FOUND:
        errorResponse.error = "La bitacora no pertenece al usuario"
        return [rcodes.UNAUTHORIZED, errorResponse]

    if ("Lon" not in object) or ("Lat" not in object):
        errorResponse.error = "Objeto Invalido"
        return [rcodes.BAD_REQUEST, errorResponse]

    element = schemas.PuntosInteres(Lat=object["Lon"], Lon=object["Lat"], UrlMedia="")
    try:
        storage = gstorage()
        response = await storage.upload_single_file(image)
        response = GoogleStorageResponse(**response)
        response.file_path = "https://storage.googleapis.com/" + response.file_path
        cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
        search = {"_id": serialice_id(bitacora_id)}
        element.UrlMedia = response.file_path
        update_rule = {"$push": {"PuntosInteres": element.model_dump()}}
        ans = cls.update_one(filter=search, update=update_rule, upsert=False)
        if ans:
            result = StatusResponse(
                ok=True,
                detail="Punto Agregado con foto en {}".format(response.file_path),
            )
            return [rcodes.ACEPTED, result]
        else:
            error = errors.Error(error="No se pudo agregar el punto", detail=None)
            return [rcodes.UNPROCESABLE, error]
    except Exception as e:
        error = errors.Error(
            error="No fue posible Agregar el punto de interes", detail=str(e)
        )
        return [rcodes.CONFLICT, error]


def grand_explorator_mode(user_id: str):
    errorResponse = errors.Error(error="", detail=None)
    if not valid_user_id(user_id):
        errorResponse.error = "El id del usuario es invalido"
        return [rcodes.BAD_REQUEST, errorResponse]

    user_id = serialice_id(user_id)
    if not user_exist(user_id):
        errorResponse.error = "No se actualizo el estatus"
        errorResponse.detail = "El usuario no existe"
        return [rcodes.NOT_FOUND, errorResponse]

    try:
        cls = Collections().get_collection(cf.USERS_COLLECTION)
        search = {"_id": user_id}
        update_params = {"$set": {"Guia": True}}
        ans = cls.update_one(filter=search, update=update_params, upsert=False)
        if ans:
            return [
                rcodes.CREATED,
                StatusResponse(ok=True, detail="El usuario ahora es un Guia"),
            ]
        else:
            errorResponse.error = "No se actualizo el estatus"
            errorResponse.detail = "El usuario no existe"
            return [rcodes.NOT_FOUND, errorResponse]
    except Exception as e:
        errorResponse.error = "ocurrio un error al actualizar el estado"
        errorResponse.detail = str(e)
        return [rcodes.CONFLICT, errorResponse]


def get_routes(route:str):
 
    cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)   
    
    query = {"Nombre": {"$regex": f".*{route}.*"}}
    routes = cls.find(query)
    route_objects = [schemas.Bitacora(**route) for route in routes]
    
    if route_objects:
        return route_objects
    else:
        return None

def get_ExplorationUser(user_id: str):
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    user_id = serialice_id(user_id)
    usr_search = {"_id": user_id}
    ans = cls.find_one(filter=usr_search)

    if ans:
        bitacoras_collection = Collections().get_collection(cf.LOGBOOK_COLLECTION)
        exploraciones_collection = Collections().get_collection(cf.EXPLORATION_COLLECTION)

        if hasattr(ans, "Bitacoras") and ans["Bitacoras"]:
            bitacoras_counts = bitacoras_collection.count_public_bitacoras(ans)
            active_bitacoras_count, total_bitacoras_count = bitacoras_counts
        else:
            active_bitacoras_count = 0
            total_bitacoras_count = 0

        explorations_count = exploraciones_collection.count_documents(
            {"Exploradores": {"$in": [ans["_id"]]}}
        )

        return {
            "active_bitacoras_count": active_bitacoras_count,
            "total_bitacoras_count": total_bitacoras_count,
            "explorations_count": explorations_count
        }

    return {
        "active_bitacoras_count": 0,
        "total_bitacoras_count": 0,
        "explorations_count": 0
    }