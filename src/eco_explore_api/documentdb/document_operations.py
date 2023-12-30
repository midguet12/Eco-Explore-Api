import eco_explore_api.config as cf
import eco_explore_api.documentdb.schemas as schemas
from eco_explore_api.documentdb.document import Collections


def create_user(Usuario: schemas.Usuarios):
    cls = Collections().get_collection(cf.USERS_COLLECTION)
    ans = cls.find_one({"Email": Usuario.Email})
    if not ans:
        ans = cls.insert_one(Usuario.model_dump())
        return ans.acknowledged
    return False
