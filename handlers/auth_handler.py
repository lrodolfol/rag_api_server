import datetime
import os
import jwt

from api_manager.my_response import MyResponse
from dao.user_dao import UserDAO
from static.LogginService import LoggerService


class AuthHandler:
    def __init__(self):
        self.logger = LoggerService("AuthHandler", "INFO")
        self.secret_key = os.getenv("TOKEN_KEY")
        self.user_dao = UserDAO()

    def auth(self, request):
        self.logger.info("AuthHandler: auth method called")

        code = request.json.get('code')
        if not code:
            self.logger.error("AuthHandler: 'code' not found in request")
            return MyResponse(400, "error: Missing code in request")

        self.logger.info(f"AuthHandler: Received code: {code}")

        if not self.validate_code(code):
            return MyResponse(400, "error: Código inválido")

        token: str = self.generate_token(code)
        return MyResponse(200, token)

    def validate_code(self, code) -> bool:
        exist = self.user_dao.find(code)
        if exist <= 0:
            return False

        return True

    def generate_token(self, code: str) -> str:
        payload = {
            "sub": "rag-server-tnn",
            "exp": datetime.datetime.now() + datetime.timedelta(hours=4),
            "iat": datetime.datetime.now(),
            "role": "admin",
            "admin": True,
            "name": "admin",
            "code": code
        }

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return token
