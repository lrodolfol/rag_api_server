class OpenIaException(Exception):
    def __init__(self, message: str):
        super().__init__(f"Falha no processo open-ia - {message}")