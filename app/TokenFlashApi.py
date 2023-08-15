import json
import logging
import os

import requests
from dotenv import load_dotenv

from app.config import settings

load_dotenv()


class Token:
    def __init__(self) -> None:
        self.TOKEN_URL = os.getenv("FLASH_API_TOKEN_URL_PROD") + "/api/v1/token"
        self.HEADERS = {
            "Authorization": f"{os.getenv('FLASH_TOKEN_AUTHORIZATION')}",
            "Content-Type": "application/json",
            "Cookie": "ROUTEID=.web2; ROUTEID=.web2",
        }

    def gerar_token(self):
        payload = {
            "login": os.getenv("FLASH_PEGASUS_AUTH_USER_PROD"),
            "senha": os.getenv("FLASH_PEGASUS_AUTH_PASSWORD_PROD"),
        }
        try:
            with requests.post(
                self.TOKEN_URL, headers=self.HEADERS, json=payload
            ) as response:
                response.raise_for_status()
                response_data = response.json()
                if "access_token" in response_data:
                    token = response_data["access_token"]
                    logging.info(
                        f"Token gerado com sucesso (código: {response.status_code})"
                    )
                    return token
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao gerar token: {e}")


if __name__ == "__main__":
    teste = Token()
    teste.gerar_token()
