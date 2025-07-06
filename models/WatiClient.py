from static.Settings import Settings

import os


class WatiClient:
    def __init__(self):
        settings: Settings = Settings()

        self.client_id = settings.wati["client_id"]
        self.base_url = settings.wati["base_url"]
        self.path_url = settings.wati["path_url"]
        self.token = os.getenv("WATI_API_KEY")
