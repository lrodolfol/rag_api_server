import hashlib
import hmac
import os
import psycopg2

from api_manager.my_response import MyResponse
from static.LogginService import LoggerService


def load_data(request) -> dict[str, str]:
    data: dict[str, str] = {
        "user_name": request.json.get("name"),
        "company_name": request.json.get("company"),
        "email": request.json.get("email"),
        "phone": request.json.get("phone")
    }

    return data


DB_CONFIG = {
    'dbname': 'tinosnegocios',
    'user': 'postgres',
    'password': '1q2w3e4r@#$',
    'host': 'localhost',
    'port': 5432
}


class Register:
    def __init__(self):
        self.key_code_access = os.getenv("KEY_CODE_ACCESS").encode()
        self.logger = LoggerService("Register", "INFO")
        self.msg_error = ''


    def register_user(self, request) -> MyResponse:
        try:
            data: dict[str, str] = load_data(request)
            code = self.generate_code_access(data)

            if self.add(data, code):
                return MyResponse(201, code)
            else:
                return MyResponse(500, f"Erro ao registrar usuário. {self.msg_error}")

        except Exception as e:
            return MyResponse(400, f"Dados inválidos")


    def generate_code_access(self, data) -> str:
        dados = f"{data['user_name'].lower().strip()}|{data['company_name'].lower().strip()}|{data['email'].lower().strip()}|{data['phone'].strip()}"
        hmac_hash = hmac.new(self.key_code_access, dados.encode(), hashlib.sha256).hexdigest()
        code = hmac_hash[:8].upper()

        return code


    def add(self, data: dict[str, str], code: str) -> bool:
        try:
            with Register._connect(self) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO ragweb.clients (name, company, email, phone, code) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                        (data['user_name'], data['company_name'], data['email'].strip().replace(" ", ""), data['phone'].strip().replace(" ", ""), code)
                    )
                    self.id = cur.fetchone()[0]
                conn.commit()

                self.logger.info(f"Client {self.id} added successfully.")
                return True
        except psycopg2.IntegrityError as e:
            self.logger.error(f"Integrity error: {e}")
            self.msg_error = "Cliente já existe"
            conn.rollback()
        except Exception as e:
            self.logger.error(f"Error adding client: {e}")
            conn.rollback()
            return False


    def _connect(self):
        return psycopg2.connect(**DB_CONFIG)