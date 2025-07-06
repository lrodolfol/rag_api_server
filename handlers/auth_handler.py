import datetime
import os
from logging import Logger

import jwt

from api_manager.my_response import MyResponse
from static.LogginService import LoggerService

SECRET_KEY: str = os.getenv("token_key")


def generate_token() -> str:
    payload = {
        "sub": "rag-server-tnn",  # identificador do usuário (subject)
        "exp": datetime.datetime.now() + datetime.timedelta(hours=4),
        "iat": datetime.datetime.now(),
        "role": "admin",
        "admin": True,
        "name": "admin"
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def validate_code(code: str) -> bool:
    try:
        with open(f"./files_source/users-coded.txt", 'r', encoding='utf-8') as file:
            lines = [linha.strip() for linha in file]

        if code in lines:
            return True
        else:
            return False

    except Exception as e:
        return False


class AuthHandler:
    def __init__(self):
        self.logger = LoggerService("AuthHandler", "INFO")

    def auth(self, request):
        self.logger.info("AuthHandler: auth method called")
        try:
            code = request.json.get('code')
            if not code:
                self.logger.error("AuthHandler: 'code' not found in request")
                return MyResponse(400, "error: Missing code in request")

            self.logger.info(f"AuthHandler: Received code: {code}")

            if not validate_code(code):
                return MyResponse(400, "error: Invalid code")

            token: str = generate_token()
            return MyResponse(200, token)

        except Exception as e:
            self.logger.error(f"Error in auth method: {str(e)}")
            return MyResponse(400, "error: Verifique os dados enviados")
