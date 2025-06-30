from marshmallow import Schema, fields, ValidationError
from api_manager.response import Response


class AskmeSchema(Schema):
    question = fields.Str(required=True,
                          error_messages={
                              'required': 'Please provide a question.',
                                          'invalid': 'Invalid question format.'
                            }
                          )


askmeSchema = AskmeSchema()


def ask_me_handler(request) -> Response:
    try:
        question = askmeSchema.load(request.json)
        if not question['question']:
            return Response(400, "Please provide a question.")

        return Response(200, "Your question has been received: {}".format(question['question']))

    except ValidationError as err:
        return Response(400, err.messages)
    except Exception as e:
        return Response(500, str(e))
