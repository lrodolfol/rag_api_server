import json
from static.LogginService import LoggerService


class IOCChatLogs:
    def __init__(self):
        self.logger = LoggerService("IOChatLogs", "INFO")


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


    def get_chat_historic(self, phone_number: str) -> list:
        try:
            messages = self.client.lrange(phone_number, 0, -1)
            return [json.loads(message) for message in messages]
        except Exception as e:
            self.logger.error(f"Error getting key {phone_number} from Redis: {str(e)}")
            return []