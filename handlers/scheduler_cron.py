import json

from dao.user_dao import UserDAO
from gateways.email.EmailServices import EmailService
from gateways.pinecone.pine_cone import PineCone
from handlers.file_source_handler import FileSourceHandler
from models.RagEmail import RagEmail
from static.LogginService import LoggerService
from static.Settings import Settings


def check_expired_user() -> None:
    user_dao = UserDAO()
    logger = LoggerService("Register", "INFO")

    users_updated = user_dao.set_expired_users()
    if users_updated:
        file_handler = FileSourceHandler()

        pinecone_service = PineCone()
        for user in users_updated:
            file_handler.delete_client_file(user.code)
            pinecone_service.delete_vectors_by_user(user.code)

        json_users = [
            {
                "name": user.name,
                "company": user.company,
                "code": user.code
            }
            for user in users_updated
        ]

        logger.info(f"Users expired and services removed: {json.dumps(json_users, indent=2, ensure_ascii=False)}")

def check_will_expired_user() -> None:
    user_dao = UserDAO()
    logger = LoggerService("Register", "INFO")

    users = user_dao.get_will_expired_users()
    if users:
        email_service = EmailService()
        settings = Settings()
        company = settings.company

        for user in users:
            message = f"""Olá {user.name},\n\nSeu período de teste gratuito de 14 dias para o SpotBot está prestes a expirar em 2 dias. 
                Após esse período, os cliente não encontrarão o seu negócio como opção de consumo em nossa platadorma.\n
                Para continuar aproveitando todos os benefícios do SpotBot, recomendamos que você adquira uma assinatura premium antes do término do seu período de teste.\n
                Se tiver alguma dúvida ou precisar de assistência, não hesite em entrar em contato conosco.\n
                Atenciosamente,\n\nEquipe {company['name']}"""
            email_model = RagEmail(
                from_=company['name'],
                to=user.email,
                subject='SpotBot - Your trial is about to expire',
                sender=company['email'],
                copy_to=company['ceo']['person_email'],
                message=message
            )
            print(f"Sending expiration email to {user.email}")
            email_service.send(email_model)
