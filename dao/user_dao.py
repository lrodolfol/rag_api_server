from datetime import timedelta, datetime

import psycopg2
from typing import Optional

from models.entitie.User import User
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
                    "SELECT count(code) FROM ragweb.clients WHERE code = %s",
                    (code,),
                )
                row = cursor.fetchone()
                return row[0] if row else 0

    def find_by_code(self, code: str) -> Optional[User]:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT *
                    FROM ragweb.clients
                    WHERE code = %s
                    """,
                    (code,),
                )
                row = cursor.fetchone()

        if not row:
            return None

        id, name, company, email, phone, code, code_used, created_at, updated_at, is_premium, free_test, expired = row

        return User(
            id=id,
            name=name,
            company=company,
            email=email,
            phone=phone,
            code=code,
            code_used=code_used,
            created_at=created_at,
            updated_at=updated_at,
            is_premium=is_premium,
            free_test=free_test,
            expired=expired
        )

    def find_by_email(self, email: str) -> Optional[User]:
        normalized_email = email.strip().lower()

        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, company, email, phone, code, code_used, created_at, updated_at, is_premium, free_test
                    FROM ragweb.clients
                    WHERE lower(email) = %s
                    """,
                    (normalized_email,),
                )
                row = cursor.fetchone()

        if not row:
            return None

        id, name, company, email, phone, code, code_used, created_at, updated_at, is_premium, free_test = row

        return User(
            id=id,
            name=name,
            company=company,
            email=email,
            phone=phone,
            code=code,
            code_used=code_used,
            created_at=created_at,
            updated_at=updated_at,
            is_premium=is_premium,
            free_test=free_test
        )

    def update_code_by_email(self, email: str, new_code: str) -> None:
        normalized_email = email.strip().lower()

        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE ragweb.clients
                    SET code = %s,
                        code_used = %s,
                        updated_at = now()
                    WHERE lower(email) = %s
                    """,
                    (new_code, False, normalized_email),
                )
            connection.commit()

    def get_will_expired_users(self) -> list[User]:
        twelve_days_ago = (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d")
        users: list[User] = []

        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT name, company, code, email FROM ragweb.clients WHERE code_used = %s and free_test = %s and is_premium = %s
                 and date(created_at) = %s""",
                    (True, True, True, twelve_days_ago),
                )
                row = cursor.fetchall()

            for record in row:
                name, company, code, email = record
                user = User(
                    id=2,
                    name=name,
                    company=company,
                    code=code,
                    email=email
                )
                users.append(user)

        return users

    def get_expired_users(self) -> list[User]:
        fifteen_days_ago = (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d")
        users: list[User] = []

        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute("""SELECT name, company, code, email FROM ragweb.clients WHERE expired = %s and code_used = %s and free_test = %s and is_premium = %s
                 and date(created_at) < %s""",
                    (False, True, True, True, fifteen_days_ago),
                )
                row = cursor.fetchall()

            for record in row:
                name, company, code, email = record
                user = User(
                    name=name,
                    company=company,
                    code=code,
                    email = email,
                )
                users.append(user)

        return users

    def set_expired_users(self) -> list[User]:
        updated_rows = 0
        fifteen_days_ago = datetime.now() - timedelta(days=15)

        users_expired = self.get_expired_users()
        if users_expired:
            with psycopg2.connect(**DB_CONFIG) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""UPDATE ragweb.clients SET expired = %s, updated_at = now() WHERE code_used = %s and free_test = %s and is_premium = %s
                     and created_at <= %s""",
                        (True, True, True, True, fifteen_days_ago),
                    )

                connection.commit()

        return users_expired

    def delete_user_by_code(self, code: str) -> None:
        with psycopg2.connect(**DB_CONFIG) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM ragweb.credit_card WHERE client_id = (SELECT id FROM ragweb.clients WHERE code = %s)",
                    (code,)
                )
                cursor.execute(
                    "DELETE FROM ragweb.clients WHERE code = %s",
                    (code,),
                )
            connection.commit()
