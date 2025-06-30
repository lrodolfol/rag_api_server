class Response:
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def to_dict(self):
        return {
            "message": self.message,
            "code": self.code
        }
