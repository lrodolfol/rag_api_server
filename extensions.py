import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from static.Settings import Settings

redis_password = os.getenv("REDIS_PASSWORD", "")
redis_host = Settings().redis

rate_limit_storage = os.getenv(
    "RATE_LIMIT_STORAGE_URI",
    f"redis://:{redis_password}@{redis_host['host']}:{redis_host['port']}"
)

limiter = Limiter(key_func=get_remote_address, storage_uri=rate_limit_storage)
