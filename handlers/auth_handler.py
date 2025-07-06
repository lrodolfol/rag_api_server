import datetime
import os
from logging import Logger

import jwt

from api_manager.my_response import MyResponse
from static.LogginService import LoggerService

SECRET_KEY: str = os.getenv("token_key")


def generate_token(code: str) -> str:
    payload = {
        "sub": "rag-server-tnn",
        "exp": datetime.datetime.now() + datetime.timedelta(hours=4),
        "iat": datetime.datetime.now(),
        "role": "admin",
        "admin": True,
        "name": "admin",
        "code": code
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


class AuthHandler:
    def __init__(self):
        self.logger = LoggerService("AuthHandler", "INFO")

    def auth(self, request):
        self.logger.info("AuthHandler: auth method called")

        code = request.json.get('code')
        if not code:
            self.logger.error("AuthHandler: 'code' not found in request")
            return MyResponse(400, "error: Missing code in request")

        self.logger.info(f"AuthHandler: Received code: {code}")

        if not self.validate_code(code):
            return MyResponse(400, "error: Invalid code")

        token: str = generate_token(code)
        return MyResponse(200, token)


    def validate_code(self, code) -> bool:
        self.logger.info("AuthHandler: reading users-coded.txt")
        with open(f"./files_source/users-coded.txt", 'r', encoding='utf-8') as file:
            lines = [linha.strip() for linha in file]

        if code in lines:
            self.logger.info("AuthHandler: code found in users-coded.txt")

            if code == "r0d0lfom":
                return True

            lines.remove(code)
            with open(f"./files_source/users-coded.txt", 'w', encoding='utf-8') as file:
                for line in lines:
                    file.write(f"{line}\n")

            return True
        else:
            return False
