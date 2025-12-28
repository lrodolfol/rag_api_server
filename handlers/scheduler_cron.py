from dao.user_dao import UserDAO
from gateways.email.EmailServices import EmailService
from handlers.io_file_handler import IOFileHandler
from models.RagEmail import RagEmail
from static.LogginService import LoggerService
from static.Settings import Settings


def check_expired_user() -> None:
    user_dao = UserDAO()
    logger = LoggerService("Register", "INFO")

    users_updated = user_dao.set_expired_users()
    if users_updated:
        io_handler = IOFileHandler()
        for user in users_updated:
            io_handler.delete(f'./{user.email}')

        io_handler.merge_directory_into_file("./files_source/clients_services", "clients_services")

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
                Após esse período, os cliente não encontrarão o seu negócio como opção de consumo em nossa platadorma.\n\n
                Para continuar aproveitando todos os benefícios do SpotBot, recomendamos que você adquira uma assinatura premium antes do término do seu período de teste.\n\n
                Se tiver alguma dúvida ou precisar de assistência, não hesite em entrar em contato conosco.\n\n
                Atenciosamente,\nEquipe {company['name']}"""
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
