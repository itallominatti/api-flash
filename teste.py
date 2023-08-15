import unittest
from unittest.mock import patch

import requests

from app.config import settings
from app.TokenFlashApi import gerar_token
from app.DadosFlash import FlashAPI
from app.database import conexao


class TestConexao(unittest.TestCase):

    @patch('app.database.psycopg2.connect')
    def test_conexao_sucesso(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [("John Doe", "123456789", "ABC123")]

        resultado = conexao("123456789")

        mock_connect.assert_called_once_with(
            dbname=settings.DB_INT_NAME,
            user=settings.DB_INT_USER,
            password=settings.DB_INT_PASS,
            host=settings.DB_INT_HOST,
            port=5432,
        )

        mock_cursor.execute.assert_called_once_with(
            f"""select nome, documento, pedido_1 from
            {settings.DB_INT_NAME}.credenciamento.dashboard_rastreio_flash where documento = '123456789';"""
        )

        mock_cursor.fetchall.assert_called_once()

        self.assertEqual(resultado, [
            {
                "nome": "John Doe",
                "documento": "123456789",
                "pedido": "ABC123"
            }
        ])

        mock_cursor.close.assert_called_once()

    @patch('app.database.psycopg2.connect')
    def test_conexao_nenhum_registro(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []

        resultado = conexao("987654321")

        mock_connect.assert_called_once_with(
            dbname=settings.DB_INT_NAME,
            user=settings.DB_INT_USER,
            password=settings.DB_INT_PASS,
            host=settings.DB_INT_HOST,
            port=5432,
        )

        mock_cursor.execute.assert_called_once_with(
            f"""select nome, documento, pedido_1 from
            {settings.DB_INT_NAME}.credenciamento.dashboard_rastreio_flash where documento = '987654321';"""
        )

        mock_cursor.fetchall.assert_called_once()

        self.assertEqual(resultado, [])

        mock_cursor.close.assert_called_once()


class TestGerarToken(unittest.TestCase):

    @patch('app.TokenFlashApi.requests.post')
    def test_gerar_token_sucesso(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "dummy_token"}

        token = gerar_token()

        mock_post.assert_called_once_with(
            f"{settings.FLASH_API_TOKEN_URL}/api/v1/token",
            headers={
                "Authorization": "f6550ac1b5cc06768da5851ad718a9e38fcf854080fb17bc767347f1b52c2dc5",
                "Content-Type": "application/json",
                "Cookie": "ROUTEID=.web2; ROUTEID=.web2",
            },
            json={
                "login": settings.FLASH_PEGASUS_AUTH_USER,
                "senha": settings.FLASH_PEGASUS_AUTH_PASSWORD,
            }
        )

        self.assertEqual(token, "dummy_token")

    @patch('app.TokenFlashApi.requests.post')
    def test_gerar_token_erro(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Erro de conexão")

        with self.assertRaises(requests.exceptions.RequestException):
            gerar_token()

        mock_post.assert_called_once_with(
            f"{settings.FLASH_API_TOKEN_URL}/api/v1/token",
            headers={
                "Authorization": "f6550ac1b5cc06768da5851ad718a9e38fcf854080fb17bc767347f1b52c2dc5",
                "Content-Type": "application/json",
                "Cookie": "ROUTEID=.web2; ROUTEID=.web2",
            },
            json={
                "login": settings.FLASH_PEGASUS_AUTH_USER,
                "senha": settings.FLASH_PEGASUS_AUTH_PASSWORD,
            }
        )


class FlashAPITest(unittest.TestCase):

    @patch('app.DadosFlash.requests.post')
    def test_buscar_dados(self, mock_post):
        # Mock response
        mock_response = {
            "hawbs": [
                {
                    "historico": [
                        {
                            "ocorrencia": "01/07/2023 12:00:00.000000",
                            "evento": "Arquivo aguardando postagem"
                        },
                        {
                            "ocorrencia": "02/07/2023 12:00:00.000000",
                            "evento": "Entrega registrada"
                        }
                    ]
                }
            ]
        }

        # Mock the post method of requests
        mock_post.return_value.json.return_value = mock_response

        # Create an instance of FlashAPI
        flash_api = FlashAPI()

        # Call the buscar_dados method
        result = flash_api.buscar_dados(123)

        # Assert the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["ocorrencia"], "01/07/2023")
        self.assertEqual(result[0]["evento"], "Arquivo aguardando postagem")
        self.assertEqual(result[1]["ocorrencia"], "02/07/2023")
        self.assertEqual(result[1]["evento"], "Entrega registrada")


if __name__ == '__main__':
    unittest.main()
