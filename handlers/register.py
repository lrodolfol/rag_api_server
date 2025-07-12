import hashlib
import hmac
import os

from api_manager.my_response import MyResponse


def load_data(request) -> [str]:
    data: [str] = []

    data["user_name"] = request.json['user_name']
    data["company_name"] = request.json['company_name']
    data["email"] = request.json['email']
    data["phone"] = request.json['phone']

    return data


class Register:
    def __init__(self):
        self.key_code_access = os.getenv("KEY_CODE_ACCESS")

    def register_user(self, request) -> MyResponse:
        try:
            data: [str] = load_data(request)

            code = self.generate_code_access(data)

            #gravar no banco de dados

            return MyResponse(201, code)

        except Exception as e:
            return MyResponse(400,f"Dados inválidos")


    def generate_code_access(self, data) -> str:
        dados = f"{data['user_name'].lower().strip()}|{data['company_name'].lower().strip()}|{data['email'].lower().strip()}|{data['phone'].strip()}"
        hmac_hash = hmac.new(self.key_code_access, dados.encode(), hashlib.sha256).hexdigest()
        code = hmac_hash[:8].upper()

        return code
