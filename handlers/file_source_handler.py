from gateways.open_ia.open_ia import OpenIaService
from gateways.pinecone.pine_cone import PineCone
from gateways.lang_chain.lang_chain import generate_chunks
from api_manager.my_response import MyResponse
from handlers.io_file_handler import IOFileHandler
from models.Service import Service
from static.LogginService import LoggerService
from dao.user_dao import UserDAO

file_name: str = 'clients_services'
def read_file() -> str:
    try:
        with open(f"./files_source/{file_name}", 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""
    except Exception as e:
        return str(e)


class FileSourceHandler:
    def __init__(self, user_code: str):
        self.pinecone: PineCone = PineCone()
        self.open_ia: OpenIaService = OpenIaService()
        self.file_path = './files_source/clients_services.md'
        self.file_updated_path = './files_source/file_updated.txt'
        self.logger = LoggerService("OpenIAService", "INFO")
        self.user_code = user_code
        self.user_dao = UserDAO()


    def read_request_to_save(self, request) -> MyResponse:
        try:
            service: Service = Service(request.json['title'], request.json['description'])
            if service.is_valid():
                file_handler = IOFileHandler()
                content: str = f"# Nome: {service.service_name}\n"
                content += f"## Dados: {service.description}\n"
                content += "\n---------\n"

                file_handler.write('clients_services', self.user_code, content, overwrite=True, extension=".md")
                file_handler.merge_directory_into_file("clients_services", f"{file_name}")

                self.save_file_source_on_pinecone()
                self.user_dao.update_user_code(self.user_code)

            return MyResponse(201, "Serviço salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Error reading request to save: {e}")
            return MyResponse(
                500,
                "Erro ao processar a requisição.Verifique se os campos'title' e 'description' estão corretos."
            )


    def save_file_source_on_pinecone(self) -> None:
        file: str = read_file()

        # gera os chunks do arquivo com langchain
        file_chunks: list[str] = generate_chunks(file)

        # gera embeddings dos chunks do arquivo com open_ia
        file_embeddings: list = self.open_ia.generate_embeddings_chunks(file_chunks)

        # salva os embeddings no pinecone
        self.pinecone.save(file_embeddings)


