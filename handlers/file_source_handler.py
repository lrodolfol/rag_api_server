from api_manager.my_response import MyResponse
from models.Service import Service
from static.LogginService import LoggerService


class FileSourceHandler:
    def __init__(self):
        self.file_path = './files_source/services.md'
        self.file_updated_path = './files_source/file_updated.txt'
        self.logger = LoggerService("OpenIAService", "INFO")

    def append_to_file(self, service: Service) -> None:
        try:
            with open(self.file_path, 'a', encoding='utf-8') as file:
                file.write("---\n\n")
                file.write(f"# {service.service_name}\n")
                file.write(f"{service.description}\n")

            with open(self.file_updated_path, 'w') as file:
                file.write("S")
        except Exception as e:
            self.logger.error(f"Error appending to file: {e}")


    def read_request_to_save(self, request) -> MyResponse:
        try:
            service: Service = Service(request.json['title'], request.json['description'])
            if service.is_valid():
                self.append_to_file(service)

            return MyResponse(201, "Serviço salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Error reading request to save: {e}")
            return MyResponse(
                500,
                "Erro ao processar a requisição.Verifique se os campos'title' e 'description' estão corretos."
            )