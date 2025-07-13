import datetime
import os
from logging import Logger

import jwt
import psycopg2

from api_manager.my_response import MyResponse
from static.LogginService import LoggerService


DB_CONFIG = {
    'dbname': 'tinosnegocios',
    'user': 'postgres',
    'password': '1q2w3e4r@#$',
    'host': 'localhost',
    'port': 5432
}


class AuthHandler:
    def __init__(self):
        self.logger = LoggerService("AuthHandler", "INFO")
        self.secret_key = os.getenv("TOKEN_KEY")

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
        exist = self.find(code)
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


    def find(cls, code) -> int:
        with cls._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT count(code) FROM ragweb.clients WHERE code = %s AND code_used = false", (code,))
                row = cur.fetchone()
                if row:
                    return row[0]

                return 0


    def _connect(self):
        return psycopg2.connect(**DB_CONFIG)