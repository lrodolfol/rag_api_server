from api_manager.my_response import MyResponse
from models.Service import Service
from static.LogginService import LoggerService


class FileSourceHandler:
    def __init__(self):
        self.file_path = './files_source/file_source.txt'
        self.file_updated_path = './files_source/file_updated.txt'
        self.logger = LoggerService("OpenIAService", "INFO")

    def append_to_file(self, service: Service) -> None:
        try:
            with open(self.file_path, 'a') as file:
                file.write(service.service_name)
                file.write(service.description)

            with open(self.file_updated_path, 'w') as file:
                file.write("S")
        except Exception as e:
            self.logger.error(f"Error appending to file: {e}")


    def read_request_to_save(self, request):
        try:
            service: Service = Service(request['title'], request['description'])
            if service.is_valid():
                self.append_to_file(service)
        except Exception as e:
            self.logger.error(f"Error reading request to save: {e}")
            return MyResponse(
                500,
                "Erro ao processar a requisição.Verifique se os campos'title' e 'description' estão corretos."
            )