class Service:
    def __init__(self, service_name, description:str):
        self.service_name = service_name
        self.description = description

    def is_valid(self):
        if self.service_name is None or self.service_name == "":
            return False
        return True
