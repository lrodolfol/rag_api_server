import os

from openai import OpenAI
from openai.types import CreateEmbeddingResponse

from gateways.open_ia.open_ia_exception import OpenIaException
from models.PayloadQuestionOpenIA import PayloadQuestionOpenIA
from static.LogginService import LoggerService
from static.Settings import Settings


def model_historic(payload_openIA: PayloadQuestionOpenIA):
    historic = []

    if payload_openIA.chat_historic is None or len(payload_openIA.chat_historic) == 0:
        return historic

    for message in payload_openIA.chat_historic:
        if message.is_user:
            historic.append({"role": "user", "content": message.text})
        else:
            historic.append({"role": "assistant", "content": message.text})

    return historic


class OpenIaService:
    def __init__(self):
        settings: Settings = Settings()

        self.api_key = os.getenv("OPEN_IA_API_KEY")
        self.model_embeddings = settings.open_ia["model_embeddings"]
        self.model_chat = settings.open_ia["model_chat"]
        self.input_guide: str = settings.open_ia["input_guide"]
        self.client = OpenAI(api_key=self.api_key)

        self.logger = LoggerService("OpenIAService", "INFO")


    def has_invalid_properties(self) -> bool:
        if self.api_key is None or self.model_embeddings is None or self.model_chat is None:
            self.logger.error("OpenIA properties are invalid")
            return True

        return False


    def generate_embeddings_question(self, question: str) ->list[float]:
        if self.has_invalid_properties():
            return[]

        response: CreateEmbeddingResponse = self.client.embeddings.create(
            input=question,
            model=self.model_embeddings
        )

        return response.data[0].embedding


    def generate_embeddings_chunks(self, lista_chunks: list[str]) -> list[dict]:
        embeddings: list = []

        if self.has_invalid_properties():
            return embeddings

        for chunk in lista_chunks:
            vector: list[float] = self.generate_vector_from_chunks(chunk)
            embeddings.append({"text": chunk, "vector": vector})

        return embeddings


    def generate_vector_from_chunks(self, chunk) -> list[float]:
        response: CreateEmbeddingResponse = self.client.embeddings.create(
            input=chunk,
            model=self.model_embeddings
        )

        vector: list[float] = response.data[0].embedding

        return vector


    def make_question(self, payload_open_ia: PayloadQuestionOpenIA, phrases: list) -> str:
        if self.has_invalid_properties() or payload_open_ia.is_invalid():
            return ""

        historic = model_historic(payload_open_ia)

        client_payload = [
                {"role": "system", "content": self.input_guide},
                *historic,
                {"role": "user", "content": f"Pergunta: {payload_open_ia.question}"},
                {"role": "system", "content": f"Trechos: {phrases}"}
            ]
        client_response = self.client.responses.create(
            model=self.model_chat,
            input=client_payload
        )

        if not client_response:
            raise OpenIaException("No choices returned from OpenAI API")

        return client_response.output_text

    def summarize_chat_historic(PayloadQuestionOpenIA: PayloadQuestionOpenIA) -> str:
        pass