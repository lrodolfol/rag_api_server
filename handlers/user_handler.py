import hashlib
import hmac
import os
from datetime import datetime, timezone
from unittest.mock import right

import psycopg2

from api_manager.my_response import MyResponse
from dao.user_dao import UserDAO
from handlers.io_file_handler import IOFileHandler
from static.LogginService import LoggerService


def load_data(request) -> dict[str, str]:
    data: dict[str, str] = {
        "user_name": request.json.get("name"),
        "company_name": request.json.get("company"),
        "email": request.json.get("email"),
        "phone": request.json.get("phone")
    }

    return data


class UserHandler:
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
            self.msg_error = "Empresa ou dados de cliente já existente"
            return MyResponse(500, f"Erro ao registrar usuǭrio. {self.msg_error}")
        except Exception as error:
            self.logger.error(f"Error registering client: {error}")
            return MyResponse(400, "Dados invǭlidos")

    def generate_code_access(self, data) -> str:
        agora_utc = datetime.now(timezone.utc)
        dados = f"""{data['user_name'].lower().strip()}|{data['company_name'].lower().strip()}|
                    {data['email'].lower().strip()}|{data['phone'].strip()}|{agora_utc}"""
        hmac_hash = hmac.new(self.key_code_access, dados.encode(), hashlib.sha256).hexdigest()
        code = hmac_hash[:8].upper()

        return code

    def get_user_by_code(self, code: str) -> MyResponse:
        try:
            user = self.user_dao.find_by_code(code)
            if not user:
                return MyResponse(404, "Usuário não encontrado")

            user_data = {
                "id": user.id,
                "name": user.name,
                "company": user.company,
                "email": user.email,
                "phone": user.phone,
                "code": user.code,
                "code_used": user.code_used,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat() if user.updated_at else None
            }

            io_handler = IOFileHandler()
            file_data = io_handler.read(f'clients_services/{user.code}.md')
            description = ''

            if file_data:
                array_data = file_data.split("Dados: ")[1]
                description = array_data.replace("-", "")

            user_data["description"] = description.strip()
            return MyResponse(200, user_data)
        except Exception as error:
            self.logger.error(f"Error retrieving user by code: {error}")
            return MyResponse(500, "Erro interno do servidor")
