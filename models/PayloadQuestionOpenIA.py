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
    def __init__(self, text: str, is_user: bool):
        self.text = text
        self.is_user = is_user