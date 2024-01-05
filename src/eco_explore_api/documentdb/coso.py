from eco_explore_api.documentdb import document
from eco_explore_api.config import USERS_COLLECTION
from eco_explore_api.documentdb.schemas import Usuarios

cp = document.Collections()


col = cp.get_collection(USERS_COLLECTION)


ejemplo = Usuarios(
    ApellidoMaterno="Sains",
    ApellidoPaterno="Guzman",
    Email="zine@gmail.com",
    Telefono="+529221534689",
    Nombre="Zine",
    PerfilPublico=True,
    UrlImagen="nada",
    Guia=False,
    Bitacoras=[],
)

print(USERS_COLLECTION)

# print(ejemplo.model_dump())
