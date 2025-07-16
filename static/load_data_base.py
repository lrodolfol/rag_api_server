import os

from static.Settings import Settings


def Load_Data_Base_Info() -> dict[str, str]:
    DB_CONFIG = {
        'dbname': '',
        'user': '',
        'password': '',
        'host': '',
        'port': 5432
    }
    settings: Settings = Settings()

    DB_CONFIG['dbname'] = settings.database["database"]
    DB_CONFIG['user'] = settings.database["user"]
    DB_CONFIG['password'] = os.getenv("DATA_BASE_PASSWORD")
    DB_CONFIG['host'] = os.getenv("DATA_BASE_HOST")
    DB_CONFIG['port'] = settings.database["port"]

    return DB_CONFIG