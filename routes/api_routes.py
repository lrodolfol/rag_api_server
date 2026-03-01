import jwt
import os
import smtplib

from email.message import EmailMessage
from functools import wraps

from flask import Blueprint, g, jsonify, request

from api_manager.my_response import MyResponse
from extensions import limiter
from handlers.ask_handler import AskMeHandler
from handlers.auth_handler import AuthHandler
from handlers.file_source_handler import FileSourceHandler
from handlers.user_credit_card_handler import UserCreditCardHandler
from handlers.user_handler import UserHandler
from handlers.password_recovery import PasswordRecoveryHandler
from models.entitie.UserCreditCard import UserCreditCard

api_blueprint = Blueprint("api", __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Missing token"}), 401

        try:
            secret_key: str = os.getenv("TOKEN_KEY")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            g.user_code = payload.get("code")
            request.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Expired token"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


@api_blueprint.route("/api/v1/home")
def hello_world():
    return "It works!"


@api_blueprint.route("/api/v1/askme", methods=["POST"])
def ask_me():
    ask_me_handler = AskMeHandler()
    response: MyResponse = ask_me_handler.ask_me_handler(request)
    return jsonify(response.to_dict()), response.code


@api_blueprint.route("/api/v1/askme-chat-online", methods=["POST"])
@limiter.limit("2/minute")
def ask_me_chat_online():
    ask_me_handler = AskMeHandler()
    response: MyResponse = ask_me_handler.ask_me_handler_chat_online(request)
    return jsonify(response.to_dict()), response.code


@api_blueprint.route("/api/v1/services", methods=["POST"])
@token_required
def services():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing authorization header"}), 401

    file_source_handler = FileSourceHandler()
    response: MyResponse = file_source_handler.read_request_to_save(g.user_code, request)

    return jsonify(response.to_dict()), response.code


@api_blueprint.route("/api/v1/validate-key", methods=["POST"])
def validate_key():
    auth_handler: AuthHandler = AuthHandler()
    response: MyResponse = auth_handler.auth(request)

    return jsonify(response.to_dict()), response.code


@api_blueprint.route("/api/v1/contact", methods=["POST"])
def send_email():
    data = request.json
    to = "tinosnegocios1@gmail.com"
    subject = data.get("subject")
    sender = data.get("sender")
    phone = data.get("phone")
    name = data.get("name")

    message = f"{data.get('message')}\n\n{name} - {phone} - {sender}"

    try:
        email = EmailMessage()
        email["From"] = f"{name} - {sender}"
        email["To"] = to
        email["Subject"] = subject
        email["Reply-To"] = sender
        email["Bcc"] = "rodolfo0ti@gmail.com"
        email.set_content(message)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            email_password: str = os.getenv("EMAIL_PASSWORD")
            smtp.login(to, email_password)
            smtp.send_message(email)

        return jsonify({"success": True}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


@api_blueprint.route("/api/v1/register", methods=["POST"])
def register():
    register_handler: UserHandler = UserHandler()
    response: MyResponse = register_handler.register_user(request)

    return jsonify(response.to_dict()), response.code


@api_blueprint.route("/api/v1/password-recovery", methods=["POST"])
def recover_password():
    recovery_handler = PasswordRecoveryHandler()
    recovery_handler.recover_password(request)
    return jsonify({"success": True}), 200

@api_blueprint.route("/api/v1/user", methods=["GET"])
@token_required
def get_user_data():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing authorization header"}), 401

    handler = UserHandler()
    response: MyResponse = handler.get_user_by_code(g.user_code)
    return jsonify(response.message), response.code

@api_blueprint.route("/api/v1/credit-card", methods=["POST"])
@token_required
def user_credit_card_register():
    body = request.get_json()
    card: UserCreditCard = UserCreditCard(
            id=body.get("id"),
            completed_name=body.get("completed_name", ""),
            number=body.get("number"),
            validity=body.get("validity", ""),
            client_id=body.get("client_id"),
        )

    result: MyResponse = UserCreditCardHandler().register_user(card)
    return jsonify(result.to_dict()), result.code


@api_blueprint.route("/api/v1/user-cancelled-account", methods=["POST"])
@token_required
def user_cancelled_account():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing authorization header"}), 401

    handler = UserHandler()
    response: MyResponse = handler.canceled_account(g.user_code)
    return jsonify(response.message), response.code

@api_blueprint.route("/api/v1/validate-token", methods=["GET"])
@token_required
def user_validate_token():
    return jsonify({"success": True}), 200