from flask import Flask, request
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)


class AskmeSchema(Schema):
    question = fields.Str(required=True,
                          error_messages={'required': 'Please provide a question.',
                                          'invalid': 'Invalid question format.'})
askmeSchema = AskmeSchema()

@app.route('/api/v1/home')
def hello_world():
    return "It's works!"


@app.route('/api/v1/askme', methods=['POST'])
def ask_me():
    try:
        question = askmeSchema.load(request.json)
        if not question['question']:
            return "Please provide a question.", 400

        print(question['question'])

        return "Ask me anything!"
    except ValidationError as err:
        return err.messages, 400
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run()
