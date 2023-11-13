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
LOGBOOK_COLLECTION = env.get_variable("LOGBOOK_COLLECTION", "Bitacora")
USERS_COLLECTION = env.get_variable("USERS_COLLECTION", "usuarios")
