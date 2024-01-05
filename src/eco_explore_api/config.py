import os
from dotenv import load_dotenv


class EnvVar:
    def __init__(self):
        try:
            load_dotenv()
        except Exception:
            pass

    def get_variable(self, name, alt="No Content"):
        try:
            value = os.getenv(name)
            return value if value else alt
        except Exception:
            return alt


# Enviroments Variables
env = EnvVar()

DOCUMENT_DB_USER = env.get_variable("DB_USER", "usuario")
DOCUMENT_DB_PASSWORD = env.get_variable("DB_PASSWORD", "contra")
DEFAULT_DATABASE = env.get_variable("DEFAULT_DATABASE", "base de datos")
DOCUMENT_DB_URL = env.get_variable("DB_URL", "localhost")
LOGBOOK_COLLECTION = env.get_variable("LOGBOOK_COLLECTION", "Bitacora")
COMENTARY_COLLECTION = env.get_variable("COMENTARY_COLLECTION", "Comentarios")
USERS_COLLECTION = env.get_variable("USERS_COLLECTION", "Usuarios")
EXPLORATION_COLLECTION = env.get_variable("EXPLORATION_COLLECTION", "Exploracion")
GOOGLE_STORAGE = env.get_variable("GOOGLE_APPLICATION_CREDENTIALS", "google")
GOOGLE_PROJECT = env.get_variable("GOOGLE_PROJECT_ID", "id")
BUCKET_NAME = env.get_variable("GOOGLE_STORAGE_BUCKET", "bucket")
GRPC_SERVER_URL = env.get_variable("GRPC_SERVER", "localhost")
SECRET_KEY_AUTH = env.get_variable("AUTH_SECRET", "1234")
AUTH_ALGORITH = env.get_variable("AUTH_ALGORITH", "sha")
