import hashlib
import hmac
import os
import secrets
from datetime import timezone, datetime
from typing import Tuple

from flask import Request

from dao.user_dao import UserDAO
from gateways.email.EmailServices import EmailService
from gateways.pinecone.pine_cone import PineCone
from handlers.io_file_handler import IOFileHandler
from models.RagEmail import RagEmail
from models.entitie.User import User
from static.LogginService import LoggerService
from static.Settings import Settings


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
        self.email_service = EmailService()
        self.setting = Settings()
        self.io_file_handler = IOFileHandler()
        self.pinecone = PineCone()

    def recover_password(self, request: Request) -> None:
        try:
            email = extract_email(request)
            user: User = self.user_dao.find_by_email(email)

            if not user:
                return None

            new_code = generate_random_code(user)
            self.user_dao.update_code_by_email(email, new_code)

            plain_message = f"""Olá {user.name},
            
            Seu novo código de acesso é: {new_code}
            
            Atenciosamente,
            Equipe {self.setting.company['name']}"""

            html_message = f"""<html>
              <body style="font-family: Arial, sans-serif; color: #1b1b1b;">
                <p>Olá {user.name},</p>
                <p>Solicitamos a geração de um novo código de acesso e ele já está pronto para ser utilizado.</p>
                <p style="font-size: 1rem; margin-top: 1rem;">Seu novo código de acesso é:</p>
                <p style="font-size: 2rem; font-weight: 700; letter-spacing: 0.1rem; color: #0b6efd; margin: 0;">
                  {new_code}
                </p>
                <p style="margin-top: 1rem;">
                  Use-o na próxima tela de login. Se você não solicitou essa alteração, entre em contato imediatamente com a equipe de segurança.
                </p>
                <p>Atenciosamente,<br/>Equipe {self.setting.company['name']}</p>
              </body>
            </html>"""

            rag_email: RagEmail = RagEmail(
                from_=self.setting.company['name'],
                to = user.email,
                subject = 'SpotBot - Novo código de acesso disponível',
                sender = self.setting.company['email'],
                copy_to = self.setting.company['ceo']['person_email'],
                message = plain_message,
                html_message = html_message
            )
            #self.email_service.send(rag_email)

            self.io_file_handler.rename_file(
                'clients_services',
                f"{user.code}.md",
                f"{new_code}.md"
            )

            content = self.io_file_handler.read(f'clients_services/{new_code}.md')

            self.pinecone.delete_vectors_by_user(user.code)
            self.pinecone.save_user_content(
                content,
                new_code,
                user.company
            )

            return None

        except ValueError as error:
            self.logger.warning(f"Password recovery failed due to invalid payload: {error}")
            return {"error": str(error)}, 400
        except Exception as error:
            self.logger.error(f"Unexpected error during password recovery: {error}")
            return {"error": "internal server error"}, 500
