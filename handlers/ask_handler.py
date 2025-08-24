import datetime

from marshmallow import ValidationError
from api_manager.my_response import MyResponse
from gateways import ChatLogsClient
from gateways.Http.RequestClient import RequestClient
from gateways.SchedulerChats import SchedulerChats
from gateways.open_ia.open_ia import OpenIaService
from gateways.pinecone.pine_cone import PineCone
from gateways.redis.RedisClient import RedisClient
from models.PayloadQuestionOpenIA import PayloadQuestionOpenIA, ChatMessage
from models.WatiClient import WatiClient
from static.LogginService import LoggerService
from datetime import datetime, timedelta, timezone

file_name: str = 'services.md'


def file_source_updated():
    try:
        with open("./files_source/file_updated.txt", 'r', encoding='utf-8') as file:
            lines = file.read()
            last_line = lines[-1] if lines else ''

            if last_line == 'S'.upper():
                return True
    except Exception:
        return False


def model_chat_historic(histotic: list[dict]) -> list[ChatMessage]:
    chat_historic: list[ChatMessage] = []

    if histotic is None or len(histotic) == 0:
        return chat_historic

    for message in histotic:
        chat_message: ChatMessage = ChatMessage(
            id=message['id'],
            text=message['text'],
            is_user=message['isUser'],
            timestamp=message['timestamp']
        )
        chat_historic.append(chat_message)

    return chat_historic


def model_historic(historic_from_redis):
    chat_historic: list[ChatMessage] = []

    if historic_from_redis is None or len(historic_from_redis) == 0:
        return chat_historic

    for message in historic_from_redis:
        chat_message: ChatMessage = ChatMessage(
            text=message['text'],
            is_user=message['is_user']
        )
        chat_historic.append(chat_message)

    return chat_historic


class AskMeHandler:
    def __init__(self):
        self.pinecone: PineCone = PineCone()
        self.open_ia: OpenIaService = OpenIaService()

        self.logger = LoggerService("AskmeHandler", "INFO")


    def ask_me_handler_chat_online(self, request) -> MyResponse:
        try:
            self.logger.info(f"Received question: {request.json}")

            question: str = request.json['text']
            chat_historic: list[ChatMessage] = model_chat_historic(request.json['historic'])

            payload_open_ia: PayloadQuestionOpenIA = PayloadQuestionOpenIA(question, chat_historic)

            # faço embeddings da pergunta com open_ia
            question_embeddings: list[float] = self.open_ia.generate_embeddings_question(question)

            # consultar pinecone (acho que o pinecone só deve ser chamado em uma nova conversação)
            get_from_pinecone = self.pinecone.get(question_embeddings)

            # gerar a pergunta com open_ia
            response: str = self.open_ia.make_question(payload_open_ia, get_from_pinecone["matches"])

            return MyResponse(200, format(f"{response}"))

        except ValidationError as e:
            self.logger.error(f"Error validating request: {e.messages}")
            return MyResponse(400, e.messages)
        except Exception as e:
            self.logger.error(f"Error validating request: {e.messages}")
            return MyResponse(500, str(e))


    def ask_me_handler(self, request) -> MyResponse:
        try:
            self.logger.info(f"Received question: {request.json}")

            question: str = request.json['text']
            user_name: str = request.json['senderName']
            user_phone: str = request.json['waId']

            #buscar o histórico de mensagens do usuário
            historic = ChatLogsClient.get_chat_historic(user_phone, use_redis=True)
            chat_historic = model_historic(historic)
            payload_open_ia: PayloadQuestionOpenIA = PayloadQuestionOpenIA(question, chat_historic)

            # faço embeddings da pergunta com open_ia
            question_embeddings: list[float] = self.open_ia.generate_embeddings_question(question)

            # consultar pinecone
            get_from_pinecone = self.pinecone.get(question_embeddings)

            # gerar a pergunta com open_ia
            response: str = self.open_ia.make_question(payload_open_ia, get_from_pinecone["matches"])

            # atualiza o histórico de mensagens do usuário
            ChatLogsClient.set_message_to_chat_historic(user_phone, question, True)
            ChatLogsClient.set_message_to_chat_historic(user_phone, response, True)

            wati_client = WatiClient()

            request_client: RequestClient = RequestClient()
            request_client.send_request(wati_client, user_phone, f"{user_name},\n{response}")

            #agenda um horario para terminar a conversa e remover os logs do chat
            sched:SchedulerChats = SchedulerChats()
            sched.finish_chat(user_phone)

            return MyResponse(200, format(f"{user_name}\n\n{response}"))

        except ValidationError as e:
            self.logger.error(f"Error validating request: {e.messages}")
            return MyResponse(400, e.messages)
        except Exception as e:
            self.logger.error(f"Error validating request: {e}")
            return MyResponse(500, str(e))
