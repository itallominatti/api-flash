import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from fastapi import HTTPException

from app.config import settings
from app.TokenFlashApi import Token

load_dotenv()

SITUACOES = {
    "Arquivo aguardando postagem": "Faturado",
    "Postado - logistica iniciada": "Faturado",
    "Emissão de CTe registrada": "Faturado",
    "CTe autorizada pelo SEFAZ": "Faturado",
    "Preparado para Redespacho": "Faturado",
    "Em arquivo-aguardando Postagem": "Faturado",
    "Preparada para a transferencia": "Faturado",
    "OBJETO Recebido": "Em preparação",
    "Comprovante registrado": "Entregue",
    "Entrega registrada via RT": "Entregue",
    "Entrega registrada": "Entregue",
    "AR digitalizada": "Entregue",
    "POD protocolado - FRANQUIA": "Entregue",
    "Preparada para a transferência": "Enviado",
    "Hawb recebida -": "Enviado",
    "Entrega em andamento (na rua)": "A caminho",
    "Envio protocolado p/ Terceiro": "A caminho",
    "Redespachado por Terceiro": "A caminho",
    "Programado Nova Tentativa": "Tentativa de entrega sem sucesso",
    "Em procedimento de retorno": "Tentativa de entrega sem sucesso",
    "Protocolado em Custodia": "Tentativa de entrega sem sucesso",
    "Telemarketing Disparado": "Tentativa de entrega sem sucesso",
    "Aguardando telemarketing": "Tentativa de entrega sem sucesso",
    "Devolucao Recebida - Avulsa": "Tentativa de entrega sem sucesso",
    "Devol.Protocolada - AO CLIENTE": "Tentativa de entrega sem sucesso",
    "Entrega NAO efetuada(RT)": "Nova tentativa de entrega",
    "Ciclo Operacional Encerrado": "Pedido não entregue",
}


class FlashAPI:
    def __init__(self):
        token = Token()
        self.authorization = token.gerar_token()

    def gerar_response(self, id):
        url_api = os.getenv("FLASH_API_TOKEN_URL_PROD") + "/padrao/v2/consulta"

        payload = json.dumps({"clienteId": 6702, "cttId": [8779], "numEncCli": [id]})

        headers = {
            "Authorization": self.authorization,
            "Content-Type": "application/json",
            "Cookie": "ROUTEID=.web2",
        }

        response = requests.post(url_api, headers=headers, data=payload)

        return response

    def formatar_datas(self, dados):
        for ocorrencia in dados:
            ocorrencia["ocorrencia"] = datetime.strptime(
                ocorrencia["ocorrencia"], "%d/%m/%Y %H:%M:%S.%f"
            ).strftime("%d/%m/%Y")
            ocorrencia["evento"] = SITUACOES.get(
                ocorrencia["evento"], ocorrencia["evento"]
            )

    def organizar_datas(self, dados):
        dados.sort(
            key=lambda date: datetime.strptime(
                date["ocorrencia"], "%d/%m/%Y %H:%M:%S.%f"
            ),
            reverse=True,
        )

    def buscar_dados(self, id) -> list:
        response = self.gerar_response(id)

        try:
            response.raise_for_status()

            dados = response.json()["hawbs"][0]["historico"]

            self.organizar_datas(dados)

            self.formatar_datas(dados)

            return dados

        except (requests.exceptions.RequestException, KeyError) as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    teste = FlashAPI()
    teste.buscar_dados(7909)
