import eco_explore_api.config as cf
from eco_explore_api.documentdb.document import Collections
import eco_explore_api.documentdb.schemas as schemas
from eco_explore_api.documentdb.document_operations import transform_id_object


def get_user(email: str):
    try:
        cls = Collections().get_collection(cf.USERS_COLLECTION)
        search = {"Email": email}
        ans = cls.find_one(filter=search)
        if ans:
            ans = transform_id_object(ans)
            # print(ans)
            return schemas.UsuariosModelAuth(**transform_id_object(ans))
        else:
            return None
    except Exception as e:
        # print(str(e))
        return None
