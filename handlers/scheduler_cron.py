from dao.user_dao import UserDAO
from static.LogginService import LoggerService


def check_expired_user() -> None:
    user_dao = UserDAO()
    logger = LoggerService("Register", "INFO")

    users_updated = user_dao.set_expired_users()
    if users_updated > 0:
        logger.info(f"Scheduler Cron: {users_updated} users set to expired.")