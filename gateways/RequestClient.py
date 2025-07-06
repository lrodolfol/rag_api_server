import requests

from models.WatiClient import WatiClient
from static.LogginService import LoggerService


class RequestClient:
    def __init__(self):
        self.logger = LoggerService("RequestClient", "INFO")

    def send_request(self, wati_client: WatiClient, phone_number: str, message: str):
        try:
            headers = {
                "Authorization": f"Bearer {wati_client.token}"
            }

            url: str = f"{wati_client.base_url}{wati_client.client_id}{wati_client.path_url}{phone_number}?messageText={message}"
            response = requests.post(
                url,
                headers=headers
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            return None