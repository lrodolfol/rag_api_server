import json

from flask import Flask, request, render_template, jsonify
from handlers.ask_handler import ask_me_handler
from api_manager.response import Response

app = Flask(__name__)


@app.route('/api/v1/home')
def hello_world():
    return "It's works!"


@app.route('/api/v1/askme', methods=['POST'])
def ask_me():
    response: Response = ask_me_handler(request)
    return jsonify(response.to_dict())


if __name__ == '__main__':
    app.run()
