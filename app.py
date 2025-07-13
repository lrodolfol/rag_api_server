import os
import smtplib

from flask import Flask
from flask_cors import CORS

from handlers.ask_handler import AskMeHandler
from api_manager.my_response import MyResponse
from handlers.auth_handler import AuthHandler
from handlers.file_source_handler import FileSourceHandler
from email.message import EmailMessage

app = Flask(__name__)
CORS(app, origins=["http://localhost:4200", "http://127.0.0.1:5500", "https://tinosnegocios.com.br"])
SECRET_KEY: str = os.getenv("TOKEN_KEY")
EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

import jwt
from flask import request, jsonify
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'error': 'Missing token'}), 401

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # você pode acessar o payload aqui se quiser
            request.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Inválid token'}), 401

        return f(*args, **kwargs)
    return decorated


@app.route('/api/v1/home')
def hello_world():
    return "It's works!"


@app.route('/api/v1/askme', methods=['POST'])
def ask_me():
    ask_me_handler = AskMeHandler()
    response: MyResponse = ask_me_handler.ask_me_handler(request)
    #return Response(response.message),200
    return jsonify(response.to_dict()), response.code


@app.route('/api/v1/services', methods=['POST'])
@token_required
def services():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Missing authorization header"}), 401
    file_source_handler = FileSourceHandler()
    response: MyResponse = file_source_handler.read_request_to_save(request)

    return jsonify(response.to_dict()), response.code


@app.route('/api/v1/validate-key', methods=['POST'])
def validate_key():
    auth_handler: AuthHandler = AuthHandler()
    response: MyResponse = auth_handler.auth(request)

    return jsonify(response.to_dict()), response.code


@app.route('/api/v1/contact', methods=['POST'])
def send_email():
    data = request.json
    to = "tinosnegocios1@gmail.com"
    subject = data.get('subject')
    sender = data.get('sender')
    phone = data.get('phone')
    name = data.get('name')

    message = f"{data.get('message')}\n\n{name} - {phone} - {sender}"

    try:
        email = EmailMessage()
        email['From'] =  f"{name} - {sender}"
        email['To'] = to
        email['Subject'] = subject
        email['Reply-To'] = sender
        email['Bcc'] = "rodolfo0ti@gmail.com"
        email.set_content(message)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(to, EMAIL_PASSWORD)
            smtp.send_message(email)

        return jsonify({ "success": True }), 200
    except Exception as e:
        return jsonify({ "error": str(e) }), 500


@app.route('/api/v1/register', methods=['POST'])
def register():
    from handlers.register import Register
    register_handler: Register = Register()
    response: MyResponse = register_handler.register_user(request)

    return jsonify(response.to_dict()), response.code


if __name__ == '__main__':
    app.run()
