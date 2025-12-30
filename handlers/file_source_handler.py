from gateways.open_ia.open_ia import OpenIaService
from gateways.pinecone.pine_cone import PineCone
from api_manager.my_response import MyResponse
from handlers.io_file_handler import IOFileHandler
from models.Service import Service
from static.LogginService import LoggerService
from dao.user_dao import UserDAO

file_name: str = 'clients_services'

class FileSourceHandler:
    def __init__(self, user_code: str):
        self.pinecone: PineCone = PineCone()
        self.open_ia: OpenIaService = OpenIaService()
        self.logger = LoggerService("OpenIAService", "INFO")
        self.user_code = user_code
        self.user_dao = UserDAO()


    def read_request_to_save(self, request) -> MyResponse:
        try:
            service: Service = Service(request.json['title'], request.json['description'])
            description_sem_linhas_em_branco = "\n".join(filter(str.strip, service.description.splitlines()))
            if service.is_valid():
                file_handler = IOFileHandler()
                content: str = f"# Nome: {service.service_name}\n"
                content += f"## Dados: {description_sem_linhas_em_branco}\n"
                content += "\n---------"

                file_handler.write('clients_services', self.user_code, content, overwrite=True, extension=".md")
                file_handler.merge_directory_into_file("clients_services", f"{file_name}")

                self.pinecone.save(file_handler.read('clients_services\\clients_services.md'))
                self.user_dao.update_user_code(self.user_code)

            return MyResponse(201, "Serviço salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Error reading request to save: {e}")
            return MyResponse(
                500,
                "Erro ao processar a requisição.Verifique se os campos'title' e 'description' estão corretos."
            )
