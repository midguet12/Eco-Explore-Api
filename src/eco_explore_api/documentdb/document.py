from eco_explore_api.config import (
    DOCUMENT_DB_PASSWORD,
    DOCUMENT_DB_USER,
    DOCUMENT_DB_URL,
    DEFAULT_DATABASE,
)
from pymongo import MongoClient


class DatabaseConnection:
    def __init__(self):
        self._CONNECTION_URI = "mongodb://{}:{}@{}/?authMechanism=DEFAULT&authSource={}&retryWrites=false".format(
            DOCUMENT_DB_USER,
            DOCUMENT_DB_PASSWORD,
            DOCUMENT_DB_URL,
            DEFAULT_DATABASE
        )
        try:
            self._client = MongoClient(self._CONNECTION_URI)
        except Exception:
            self._client = None

    def get_client(self):
        return self._client


class Collections:
    def __init__(self):
        self._client = DatabaseConnection()

    def get_collection(self, collection_name: str):
        if (
            len(self._client.list_databases)
            and len(collection_name)
            and isinstance(collection_name, str)
        ):
            return self._client[collection_name]
