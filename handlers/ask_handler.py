import hashlib
import json

from marshmallow import Schema, fields, ValidationError
from openai import embeddings
from pinecone.core.openapi.db_data.model.query_response import QueryResponse

from api_manager.my_response import MyResponse
from gateways.lang_chain.lang_chain import generate_chunks
from gateways.open_ia.open_ia import OpenIaService
from gateways.pinecone.pine_cone import PineCone


file_name: str = 'services.md'


def read_file() -> str:
    try:
        with open(f"./files_source/{file_name}", 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return str(e)


class AskMeHandler:
    def __init__(self):
        self.pinecone: PineCone = PineCone()
        self.open_ia: OpenIaService = OpenIaService()

    def ask_me_handler(self, request) -> MyResponse:
        try:
            question: dict[str] = request.json['question']

            # ====================================
            # =processo para salvar arquivo fonte=
            # =ter alguma forma de avisar que o arquivo foi modificado=
            # ====================================
            # le o arquivo fonte
            file: str = read_file()
            if not file:
                return MyResponse(500, "Error reading file. File not found or empty.")

            # gera os chunks do arquivo com langchain
            file_chunks: list[str] = generate_chunks(file)
            if not file_chunks:
                return MyResponse(500, "Error generating chunks from the file.")

            # gera embeddings dos chunks do arquivo com open_ia
            file_embeddings:list = self.open_ia.generate_embeddings_chunks(file_chunks)

            #salva os embeddings no pinecone
            self.pinecone.save(file_embeddings)




            # ====================================
            # = processo gerar a pergunta ========
            # ====================================
            # faço embeddings da pergunta com open_ia
            question_embeddings: list[float] = self.open_ia.generate_embeddings_question(question) #tipagem do embeddings

            # consultar pinecone
            get_from_pinecone = self.pinecone.get(question_embeddings)

            # gerar a pergunta com open_ia
            response: str = self.open_ia.make_question(question, get_from_pinecone["matches"])

            return MyResponse(200, format(response))

        except ValidationError as err:
            return MyResponse(400, err.messages)
        except Exception as e:
            return MyResponse(500, str(e))
