import psycopg2
from gateways.open_ia.open_ia import OpenIaService
from gateways.pinecone.pine_cone import PineCone
from gateways.lang_chain.lang_chain import generate_chunks
from api_manager.my_response import MyResponse
from models.Service import Service
from static.LogginService import LoggerService

DB_CONFIG = {
    'dbname': 'tinosnegocios',
    'user': 'postgres',
    'password': '1q2w3e4r@#$',
    'host': 'localhost',
    'port': 5432
}

file_name: str = 'services.md'
def read_file() -> str:
    try:
        with open(f"./files_source/{file_name}", 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return str(e)


class FileSourceHandler:
    def __init__(self):
        self.pinecone: PineCone = PineCone()
        self.open_ia: OpenIaService = OpenIaService()
        self.file_path = './files_source/services.md'
        self.file_updated_path = './files_source/file_updated.txt'
        self.logger = LoggerService("OpenIAService", "INFO")


    def read_request_to_save(self, request, user_code: str) -> MyResponse:
        try:
            service: Service = Service(request.json['title'], request.json['description'])
            if service.is_valid():
                self.append_to_file(service)

                self.update_user_code(user_code)

            return MyResponse(201, "Serviço salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Error reading request to save: {e}")
            return MyResponse(
                500,
                "Erro ao processar a requisição.Verifique se os campos'title' e 'description' estão corretos."
            )


    def append_to_file(self, service: Service) -> None:
        try:
            with open(self.file_path, 'a', encoding='utf-8') as file:
                file.write("---\n\n")
                file.write(f"# {service.service_name}\n")
                file.write(f"{service.description}\n")

                self.save_file_source_on_pinecone()
        except Exception as e:
            self.logger.error(f"Error appending to file: {e}")


    def save_file_source_on_pinecone(self) -> None:
        file: str = read_file()

        # gera os chunks do arquivo com langchain
        file_chunks: list[str] = generate_chunks(file)

        # gera embeddings dos chunks do arquivo com open_ia
        file_embeddings: list = self.open_ia.generate_embeddings_chunks(file_chunks)

        # salva os embeddings no pinecone
        self.pinecone.save(file_embeddings)


    def update_user_code(cls, user_code):
        with cls._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE ragweb.clients SET code_used = %s, updated_at = now() WHERE code = %s",
                    (True, user_code)
                )
            conn.commit()


    def _connect(self):
        return psycopg2.connect(**DB_CONFIG)
