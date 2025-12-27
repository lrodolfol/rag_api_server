import hashlib
import hmac
import os
import psycopg2

from api_manager.my_response import MyResponse
from dao.user_dao import UserDAO
from static.LogginService import LoggerService


def load_data(request) -> dict[str, str]:
    data: dict[str, str] = {
        "user_name": request.json.get("name"),
        "company_name": request.json.get("company"),
        "email": request.json.get("email"),
        "phone": request.json.get("phone")
    }

    return data


class Register:
    def __init__(self):
        self.key_code_access = os.getenv("KEY_CODE_ACCESS").encode()
        self.logger = LoggerService("Register", "INFO")
        self.msg_error = ''
        self.user_dao = UserDAO()

    def register_user(self, request) -> MyResponse:
        try:
            data: dict[str, str] = load_data(request)
            code = self.generate_code_access(data)
            user_id = self.user_dao.add_user(data, code)

            self.logger.info(f"Client {user_id} added successfully.")
            return MyResponse(201, code)
        except psycopg2.IntegrityError as error:
            self.logger.error(f"Integrity error: {error}")
            self.msg_error = "Empresa ou dados de cliente jǭ existente"
            return MyResponse(500, f"Erro ao registrar usuǭrio. {self.msg_error}")
        except Exception as error:
            self.logger.error(f"Error registering client: {error}")
            return MyResponse(400, "Dados invǭlidos")

    def generate_code_access(self, data) -> str:
        dados = f"{data['user_name'].lower().strip()}|{data['company_name'].lower().strip()}|{data['email'].lower().strip()}|{data['phone'].strip()}"
        hmac_hash = hmac.new(self.key_code_access, dados.encode(), hashlib.sha256).hexdigest()
        code = hmac_hash[:8].upper()

        return code
