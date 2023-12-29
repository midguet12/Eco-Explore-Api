from eco_explore_api.config import (
    DOCUMENT_DB_PASSWORD,
    DOCUMENT_DB_USER,
    DOCUMENT_DB_URL,
    DEFAULT_DATABASE,
)
from pymongo import MongoClient


class DatabaseConnection:
    def __init__(self, database: str = DEFAULT_DATABASE):
        self._CONNECTION_URI = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority".format(
            DOCUMENT_DB_USER, DOCUMENT_DB_PASSWORD, DOCUMENT_DB_URL
        )
        try:
            self._client = MongoClient(self._CONNECTION_URI)
            self._client = self._client[database]
        except Exception as e:
            self._client = str(e)

    def get_client(self):
        return self._client


class Collections:
    def __init__(self):
        self._client = DatabaseConnection()

    def get_collection(self, collection_name: str):
        if len(collection_name) and isinstance(collection_name, str):
            return self._client[collection_name]
