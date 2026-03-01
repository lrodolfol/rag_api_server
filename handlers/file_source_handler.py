from gateways.bucket.BucketClient import BucketClient
from gateways.pinecone.pine_cone import PineCone
from api_manager.my_response import MyResponse
from models.Service import Service
from static.LogginService import LoggerService
from dao.user_dao import UserDAO


class FileSourceHandler:
    def __init__(self):
        self.pinecone: PineCone = PineCone()
        self.logger = LoggerService("OpenIAService", "INFO")
        self.user_dao = UserDAO()


    def delete_client_file(self, user_code: str) -> None:
        bucket_client = BucketClient()
        bucket_client.delete_file_client(user_code)



    def read_request_to_save(self, user_code: str, request) -> MyResponse:
        try:
            service: Service = Service(request.json['title'], request.json['description'])
            description_without_line_blanks = "\n".join(filter(str.strip, service.description.splitlines()))

            if service.is_valid():
                bucket_client = BucketClient()
                content: str = f"# Nome: {service.service_name}\n"
                content += f"## Dados: {description_without_line_blanks}\n"
                content += "---------"

                bucket_client.upload_string_client_file(content, user_code)

                self.pinecone.save_user_content(content, user_code, request.json['title'])
                self.user_dao.update_user_code(user_code)

            return MyResponse(201, "Serviço salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Error reading request to save: {e}")
            return MyResponse(
                500,
                "Erro ao processar a requisição.Verifique se os campos'title' e 'description' estão corretos."
            )


    def read_client_file(self, user_code: str) -> str:
        bucket_client = BucketClient()
        return bucket_client.read_client_file(user_code)
            

    def rename_client_file(self, old_user_code: str, new_user_code: str) -> None:
        bucket_client = BucketClient()
        bucket_client.rename_file_client(old_user_code, new_user_code)