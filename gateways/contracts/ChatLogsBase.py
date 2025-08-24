from abc import ABC, abstractmethod

class ChatLogsBase(ABC):
    @abstractmethod
    def set_message_to_chat_historic(self, phone_number: str, value: str, is_user: bool) -> bool:
        pass

    @abstractmethod
    def get_chat_historic(self, phone_number: str) -> list:
        pass

