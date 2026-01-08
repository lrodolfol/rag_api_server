import psycopg2

from models.entitie.UserCreditCard import UserCreditCard
from static.load_data_base import Load_Data_Base_Info

DB_CONFIG = Load_Data_Base_Info()


class UserCreditCardDAO:
    def add(self, user_credit_card: UserCreditCard) -> int:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO ragweb.credit_card (completed_name, number, validity, client_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (
                        user_credit_card.completed_name,
                        user_credit_card.number,
                        user_credit_card.validity,
                        user_credit_card.client_id
                    ),
                )
                id = cursor.fetchone()[0]
            connection.commit()

        return id