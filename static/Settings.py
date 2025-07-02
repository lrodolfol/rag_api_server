import json


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            with open("configuration/config.json") as file:
                data = json.load(file)
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._open_ia = data["open_ai"]
            cls._instance._pinecone = data["pinecone"]

        return cls._instance

    @property
    def open_ia(self):
        return self._open_ia.copy()

    @property
    def pinecone(self):
        return self._pinecone.copy()