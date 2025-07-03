import json

from flask import Flask, request, Response, jsonify
from handlers.ask_handler import AskMeHandler
from api_manager.my_response import MyResponse

app = Flask(__name__)

@app.route('/api/v1/home')
def hello_world():
    return "It's works!"


@app.route('/api/v1/askme', methods=['POST'])
def ask_me():
    ask_me_handler = AskMeHandler()
    response: MyResponse = ask_me_handler.ask_me_handler(request)
    #return Response(response.message),200
    return jsonify(response.to_dict()), response.code


if __name__ == '__main__':
    app.run()
