from gateways.IO.IOChatLogs import IOCChatLogs
from gateways.contracts.ChatLogsBase import ChatLogsBase
from gateways.redis.RedisClient import RedisClient


def get_chat_historic(phone_number: str, use_redis: bool = True) -> list:
    chat_logs: ChatLogsBase

    if use_redis:
        chat_logs = RedisClient()
    else:
        chat_logs = IOCChatLogs()

    return chat_logs.get_chat_historic(phone_number)


def set_message_to_chat_historic(phone_number: str, value: str, is_user: bool, use_redis: bool = True):
    chat_logs: ChatLogsBase

    if use_redis:
        chat_logs = RedisClient()
    else:
        chat_logs = IOCChatLogs()

    logs = chat_logs.set_message_to_chat_historic(phone_number, value, is_user)

    return logs