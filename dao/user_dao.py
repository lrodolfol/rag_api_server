import psycopg2

from static.load_data_base import Load_Data_Base_Info

DB_CONFIG = Load_Data_Base_Info()


class UserDAO:
    def update_user_code(self, user_code: str) -> None:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE ragweb.clients SET code_used = %s, updated_at = now() WHERE code = %s",
                    (True, user_code),
                )
            connection.commit()

    def add_user(self, data: dict[str, str], code: str) -> int:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO ragweb.clients (name, company, email, phone, code) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                    (
                        data["user_name"],
                        data["company_name"],
                        data["email"].strip().replace(" ", ""),
                        data["phone"].strip().replace(" ", ""),
                        code,
                    ),
                )
                user_id = cursor.fetchone()[0]
            connection.commit()

        return user_id

    def find(self, code: str) -> int:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT count(code) FROM ragweb.clients WHERE code = %s AND code_used = false",
                    (code,),
                )
                row = cursor.fetchone()
                return row[0] if row else 0
