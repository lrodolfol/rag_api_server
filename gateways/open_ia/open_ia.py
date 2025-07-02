import os

from openai import OpenAI
from gateways.open_ia.open_ia_exception import OpenIaException
from static.Settings import Settings


class OpenIaService:
    def __init__(self):
        settings: Settings = Settings()

        self.api_key = os.getenv("OPEN_IA_API_KEY")
        self.model_embeddings = settings.open_ia["model_embeddings"]
        self.model_chat = settings.open_ia["model_chat"]
        self.input_guide = settings.open_ia["input_guide"]
        self.client = OpenAI(api_key=self.api_key)


    def generate_embeddings(self, question: str, chunks): #tipagem do chunks #retorna embeddings com tipagem
        if self.has_invalid_properties():
            raise OpenIaException("Invalid properties provided for embeddings generation.")


        embeddings = [] #colocar tipagem
        for chunk in chunks:
            resposta = self.client.embeddings.create(
                input=chunk,
                model=self.model_embeddings
            )
            vetor = resposta.data[0].embedding #tipagem do vetor
            embeddings.append({"texto": chunk, "vetor": vetor})

        return embeddings


    def has_invalid_properties(self) -> bool:
        if self.api_key is None or self.model_embeddings is None or self.model_chat is None:
            return False

        return True