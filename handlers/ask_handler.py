from marshmallow import Schema, fields, ValidationError
from openai import embeddings

from api_manager.my_response import MyResponse
from gateways.lang_chain.lang_chain import generate_chunks
from gateways.open_ia.open_ia import OpenIaService


class AskmeSchema(Schema):
    question = fields.Str(required=True,
                          error_messages={
                              'required': 'Please provide a question.',
                                          'invalid': 'Invalid question format.'
                            }
                          )


askmeSchema = AskmeSchema()


def ask_me_handler(request) -> MyResponse:
    try:
        question_dic: dict[str] = askmeSchema.load(request.json)

        if not question_dic['question']:
            return MyResponse(400, "Please provide a question.")

        question: str = question_dic['question']
        chunks = generate_chunks(question)  # colcoar tipagem do chunks

        open_ia: OpenIaService = OpenIaService()
        embeddings = open_ia.generate_embeddings_question(question)

        return MyResponse(200, "Your question has been received: {}".format(question))

    except ValidationError as err:
        return MyResponse(400, err.messages)
    except Exception as e:
        return MyResponse(500, str(e))
