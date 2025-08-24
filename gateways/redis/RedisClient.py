import os

import redis
import json

from gateways.contracts.ChatLogsBase import ChatLogsBase
from static.LogginService import LoggerService
from static.Settings import Settings


class RedisClient(ChatLogsBase):
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        settings: Settings = Settings()

        self.client = redis.Redis(
            host=settings.redis["host"],
            port=settings.redis["port"],
            db=settings.redis["db"],
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

        self.logger = LoggerService("RedisClient", "INFO")


    def set_message_to_chat_historic(self, phone_number: str, value: str, is_user: bool) -> bool:
        try:
            content = {
                "is_user": is_user,
                "text": value
            }
            self.client.rpush(phone_number, json.dumps(content,ensure_ascii=False))
            return True
        except Exception as e:
            self.logger.error(f"Error setting key {phone_number} in Redis: {str(e)}")
            return False
        finally:
            self.client.close()


    def get_chat_historic(self, phone_number: str) -> list:
        try:
            messages = self.client.lrange(phone_number, 0, -1)
            list_messages = [json.loads(message) for message in messages]
            return list_messages
        except Exception as e:
            self.logger.error(f"Error getting key {phone_number} from Redis: {str(e)}")
            return []
        finally:
            self.client.close()


    def clear_chat_historic(self, phone_number: str) -> bool:
        pass

    def close(self):
        try:
            self.client.close()
        except Exception as e:
            self.logger.error(f"Error closing Redis client: {str(e)}")