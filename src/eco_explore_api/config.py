import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


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


env = EnvVar()


class Settings(BaseSettings):
    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorithms: str
    class Config:
        env_file = ".env"


def get_settings():
    return Settings()


# Enviroments Variables


DOCUMENT_DB_USER = env.get_variable("DB_USER", "usuario")
DOCUMENT_DB_PASSWORD = env.get_variable("DB_PASSWORD", "contra")
LOGBOOK_COLLECTION = env.get_variable("LOGBOOK_COLLECTION", "Bitacora")
USERS_COLLECTION = env.get_variable("USERS_COLLECTION", "usuarios")
DEFAULT_DATABASE = env.get_variable("DEFAULT_DATABASE", "base de datos")
DOCUMENT_DB_URL = env.get_variable("DB_URL", "localhost")
TOKEN_AUTH = env.get_variable("AUTH0_TOKEN")
AUTH0_DOMAIN = env.get_variable("AUTH0_DOMAIN")
AUTH0_API_AUDIENCE = env.get_variable("AUTH0_API_AUDIENCE")
AUTH0_ISSUER = env.get_variable("AUTH0_ISSUER")
AUTH0_ALGORITHMS = env.get_variable("AUTH0_ALGORITHMS")
