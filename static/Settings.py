import json
import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            environment = os.getenv("ENVIRONMENT", "dev").lower()
            with open(f"configuration/config.{environment}.json", encoding="utf-8") as file:
                data = json.load(file)

            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._open_ia = data["open_ai"]
            cls._instance._pinecone = data["pinecone"]
            cls._instance._wati = data["wati"]
            cls._instance._database = data["database"]
            cls._instance._redis = data["redis"]
            cls._instance._company = data["company"]
            cls._instance._bucket = data["bucket"]

        return cls._instance

    @property
    def open_ia(self):
        return self._open_ia.copy()

    @property
    def pinecone(self):
        return self._pinecone.copy()

    @property
    def wati(self):
        return self._wati.copy()

    @property
    def database(self):
        return self._database.copy()

    @property
    def redis(self):
        return self._redis.copy()

    @property
    def company(self):
        return self._company.copy()

    @property
    def bucket(self):
        return self._bucket.copy()