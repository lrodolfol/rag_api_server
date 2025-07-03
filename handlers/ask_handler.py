from marshmallow import Schema, fields, ValidationError
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


def file_source_updated():
    try:
        with open("./files_source/file_updated.txt", 'w', encoding='utf-8') as file:
            lines = file.readlines()
            last_line = lines[-1] if lines else ''

            if last_line == '' or last_line == 'S':
                return True
    except Exception:
        return False


class AskMeHandler:
    def __init__(self):
        self.pinecone: PineCone = PineCone()
        self.open_ia: OpenIaService = OpenIaService()
        self.file_updated_path = './files_source/file_updated.txt'


    def ask_me_handler(self, request) -> MyResponse:
        try:
            question: str = request.json['question']

            if file_source_updated():
                self.save_file_source_on_pinecone()

            # faço embeddings da pergunta com open_ia
            question_embeddings: list[float] = self.open_ia.generate_embeddings_question(question)

            # consultar pinecone
            get_from_pinecone = self.pinecone.get(question_embeddings)

            # gerar a pergunta com open_ia
            response: str = self.open_ia.make_question(question, get_from_pinecone["matches"])

            return MyResponse(200, format(response))

        except ValidationError as err:
            return MyResponse(400, err.messages)
        except Exception as e:
            return MyResponse(500, str(e))

    def save_file_source_on_pinecone(self) -> None:
        file: str = read_file()

        # gera os chunks do arquivo com langchain
        file_chunks: list[str] = generate_chunks(file)

        # gera embeddings dos chunks do arquivo com open_ia
        file_embeddings: list = self.open_ia.generate_embeddings_chunks(file_chunks)

        # salva os embeddings no pinecone
        self.pinecone.save(file_embeddings)

        try:
            with open(self.file_updated_path, 'w') as f:
                f.write("N")
        except Exception as e:
            self.logger.error(f"Error updating file_updated.txt: {e}")