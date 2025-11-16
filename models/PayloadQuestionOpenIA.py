from langchain_core.messages import ChatMessage


class PayloadQuestionOpenIA:
    def __init__(self, question: str, chat_historic: list[ChatMessage]):
        self.question = question
        self.chat_historic = chat_historic

    def is_invalid(self):
        if self.question is None or self.question.strip() == "":
            return True

        return False


class ChatMessage:
    def __init__(self, id: int, text: str, is_user: bool, timestamp: str):
        self.id = id
        self.text = text
        self.is_user = is_user
        self.timestamp = timestamp