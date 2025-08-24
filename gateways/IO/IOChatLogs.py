import json

from gateways.contracts.ChatLogsBase import ChatLogsBase
from static.LogginService import LoggerService


class IOCChatLogs(ChatLogsBase):
    def __init__(self):
        self.logger = LoggerService("IOChatLogs", "INFO")
        self.log_dir = "./files_source/chat_historic/"


    def set_message_to_chat_historic(self, phone_number: str, value: str, is_user: bool) -> bool:
        try:
            content = {
                "is_user": is_user,
                "text": value
            }
            log_path = f"{self.log_dir}{phone_number}.log"

            with open(log_path, "a+", encoding="utf-8") as log_file:
                log_file.write(json.dumps(content) + "\n")
            return True
        except Exception as e:
            self.logger.error(f"Error setting key {phone_number} in Redis: {str(e)}")
            return False


    def get_chat_historic(self, phone_number: str) -> list:
        try:
            log_path = f"{self.log_dir}{phone_number}.log"
            messages = []
            with open(log_path, "a+", encoding="utf-8") as log_file:
                for line in log_file:
                    messages.append(json.loads(line.strip()))
            return messages
        except Exception as e:
            self.logger.error(f"Error getting chat historic for {phone_number}: {str(e)}")
            return []


    def clear_chat_historic(self, phone_number: str) -> bool:
        pass