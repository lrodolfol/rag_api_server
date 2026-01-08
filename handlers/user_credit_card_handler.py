import os

import psycopg2

from api_manager.my_response import MyResponse
from dao.user_credit_card_dao import UserCreditCardDAO
from models.entitie.UserCreditCard import UserCreditCard
from static.LogginService import LoggerService


class UserCreditCardHandler:
    def __init__(self):
        self.key_code_access = os.getenv("KEY_CODE_ACCESS").encode()
        self.logger = LoggerService("Register", "INFO")
        self.msg_error = ''
        self.user_credit_card_dao = UserCreditCardDAO()

    def register_user(self, user_credit_card: UserCreditCard) -> MyResponse:
        try:
            self.user_credit_card_dao.add(user_credit_card)

            self.logger.info(f"Client credit card added successfully.")
            return MyResponse(201, "Cartão de crédito registrado com sucesso.")
        except psycopg2.errors.ForeignKeyViolation as error:
            self.logger.error(f"Foreign key error: {error}")
            self.msg_error = "Cliente informado não existe"
            return MyResponse(500, f"Erro ao registrar cartão do cliente. {self.msg_error}")
        except psycopg2.errors.UniqueViolation as error:
            self.logger.error(f"Unique constraint error: {error}")
            self.msg_error = "Cartão de crédito já existente"
            return MyResponse(500, f"Erro ao registrar cartão do cliente. {self.msg_error}")
        except psycopg2.IntegrityError as error:
            self.logger.error(f"Integrity error: {error}")
            self.msg_error = "Erro de integridade ao processar o cartão"
            return MyResponse(500, f"Erro ao registrar cartão do cliente. {self.msg_error}")
        except Exception as error:
            self.logger.error(f"Error registering client: {error}")
            return MyResponse(400, "Dados inválidos")
