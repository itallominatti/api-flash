import responses
import os
from app.TokenFlashApi import Token
import logging
import requests

@responses.activate
def test_gerar_token_success():
    url = os.getenv("FLASH_API_TOKEN_URL_PROD") + "/api/v1/token"
    responses.add(responses.POST, url, json={"access_token": "token"}, status=200)

    token_instance = Token()
    token = token_instance.gerar_token()

    assert token == "token"

@responses.activate
def test_gerar_token_failure():
    url = os.getenv("FLASH_API_TOKEN_URL_PROD") + "/api/v1/token"
    responses.add(responses.POST, url, json={"error": "Unauthorized"}, status=401)

    token_instance = Token()
    token = token_instance.gerar_token()

    assert token is None

@responses.activate
def test_gerar_token_request_exception():
    url = os.getenv("FLASH_API_TOKEN_URL_PROD") + "/api/v1/token"

    def request_exception(_):
        raise requests.exceptions.RequestException("An error occurred")

    responses.add_callback(responses.POST, url, callback=request_exception)

    token_instance = Token()
    token = token_instance.gerar_token()

    assert token is None

@responses.activate
def test_gerar_token_missing_access_token():
    url = os.getenv("FLASH_API_TOKEN_URL_PROD") + "/api/v1/token"
    responses.add(responses.POST, url, json={"message": "No token provided"}, status=200)

    token_instance = Token()
    token = token_instance.gerar_token()

    assert token is None