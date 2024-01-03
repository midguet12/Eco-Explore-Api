import eco_explore_api.config as cf
import eco_explore_api.documentdb.schemas as schemas
from eco_explore_api.documentdb.document import Collections

from typing import List, Optional


def create_user(Usuario: schemas.Usuarios):
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    ans = cls.find_one({"Email": Usuario.Email})
    if not ans:
        ans = cls.insert_one(Usuario.model_dump())
        return ans.acknowledged
    return False


def get_routes(Route: schemas.Bitacora) -> Optional[List[schemas.Bitacora]]:
    cls = Collections().get_collection(cf.LOGBOOK_COLLECTION)
    
    query = {"Nombre": {"$regex": f".*{Route.Nombre}.*"}}
    routes = cls.find(query)

    route_objects = [schemas.Bitacora.model_load(route) for route in routes]

    if route_objects:
        return route_objects
    else:
        return None

from bson import ObjectId 

def get_ExplorationUser(Usuario: schemas.Usuarios) -> List[int]:
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    
    user_id = ObjectId(Usuario.id)

    ans = cls.find_one({"_id": user_id})

    if ans:
        user_instance = schemas.Usuarios(**ans)

        bitacoras_collection = Collections().get_collection(cf.LOGBOOK_COLLECTION)
        exploraciones_collection = Collections().get_collection(cf.EXPLORATIONS_COLLECTION)

        active_bitacoras_count = Bitacora.count_public_bitacoras(
            bitacoras_collection.find({"_id": {"$in": user_instance.Bitacoras}})
        )

        total_bitacoras_count = bitacoras_collection.count_documents(
            {"_id": {"$in": user_instance.Bitacoras}}
        )

        explorations_count = exploraciones_collection.count_documents(
            {"Exploradores": {"$in": [user_instance.id]}}
        )

        return [active_bitacoras_count, total_bitacoras_count, explorations_count]

    return [0, 0, 0]
