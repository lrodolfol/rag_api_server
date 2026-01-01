import hashlib
import hmac
import os
import secrets
from datetime import timezone, datetime
from typing import Tuple

from flask import Request

from dao.user_dao import UserDAO
from models.entitie.User import User
from static.LogginService import LoggerService


def generate_random_code(user: User) -> str:
    agora_utc = datetime.now(timezone.utc)
    dados = f"""{user.name.lower().strip()}|{user.company.lower().strip()}|
                {user.email.lower().strip()}|{user.phone.strip()}|{agora_utc}"""
    hmac_hash = hmac.new(os.getenv("KEY_CODE_ACCESS").encode(), dados.encode(), hashlib.sha256).hexdigest()
    code = hmac_hash[:8].upper()

    return code


def extract_email(request: Request) -> str:
    payload = request.json or {}
    email = payload.get("email")
    if not email:
        raise ValueError("Email is required")

    return email.strip()


class PasswordRecoveryHandler:
    def __init__(self):
        self.logger = LoggerService("PasswordRecovery", "INFO")
        self.user_dao = UserDAO()

    def recover_password(self, request: Request) -> None:
        try:
            email = extract_email(request)
            user: User = self.user_dao.find_by_email(email)

            if not user:
                return None

            new_code = generate_random_code(user)
            self.user_dao.update_code_by_email(email, new_code)
            # enviar novo código por email

            return None

        except ValueError as error:
            self.logger.warning(f"Password recovery failed due to invalid payload: {error}")
            return {"error": str(error)}, 400
        except Exception as error:
            self.logger.error(f"Unexpected error during password recovery: {error}")
            return {"error": "internal server error"}, 500
