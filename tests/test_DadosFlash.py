import json
from datetime import datetime

import pytest
from requests.exceptions import HTTPError, RequestException

from app.DadosFlash import SITUACOES, FlashAPI, HTTPException


@pytest.fixture
def flash_api():
    return FlashAPI()


@pytest.mark.dados_flash
# Teste para verificar se a função gerar_response está retornando 200 quando eu atribuo um id valido
def test_gerar_response_retorna_200_quando_passo_id_valido():
    flash_api = FlashAPI()
    id_valido = 7909
    response = flash_api.gerar_response(id_valido)
    assert response.status_code == 200


@pytest.mark.dados_flash
# Teste para verificar se a função gerar_response está retornando 500 quando eu atribuo um id inválido
def test_gerar_response_retorna_500_quando_passo_id_invalido():
    flash_api = FlashAPI()
    id_invalido = 123456789
    with pytest.raises(HTTPException) as exc_info:
        flash_api.buscar_dados(id_invalido)

    assert exc_info.value.status_code == 500
    assert exc_info.type == HTTPException


@pytest.mark.dados_flash
# Teste para verificar se o formato da data é em barras
def teste_verificar_se_o_formato_da_data_esta_vindo_com_barras():
    flash_api = FlashAPI()
    dados = flash_api.gerar_response(7909)
    data = dados.json()["hawbs"][0]["historico"][0]["ocorrencia"]
    assert "/" in data


@pytest.mark.dados_flash
# Teste para ver se a funcao formatar_data está formatando a data corretamente
def test_verificar_se_a_funcao_formatar_data_remove_o_horario():
    flash_api = FlashAPI()
    mock_dados = [
        {
            "ocorrencia": "27/07/2023 17:32:00.000",
            "eventoId": "2000",
            "evento": "Faturado",
            "arCorreios": "",
            "frq": "ILG",
            "local": "LONDRINA",
        }
    ]
    flash_api.formatar_datas(mock_dados)
    assert mock_dados[0]["ocorrencia"] == "27/07/2023"
    assert mock_dados[0]["evento"] == "Faturado"


@pytest.mark.dados_flash
# Teste para verificar se a funcao organizar_datas está organizando as datas de forma cronologica reversa
def test_verificar_se_a_funcao_organizar_datas_esta_organizando_as_datas_de_forma_cronologica_reversa():
    flash_api = FlashAPI()
    mock_dados = [
        {
            "ocorrencia": "30/07/2023 17:32:00.000",
            "eventoId": "4100",
            "evento": "A caminho",
            "arCorreios": "",
            "frq": "VMG",
            "local": "SAO PAULO",
        },
        {
            "ocorrencia": "26/07/2023 17:32:00.000",
            "eventoId": "3000",
            "evento": "Em preparação",
            "arCorreios": "",
            "frq": "VMG",
            "local": "SAO PAULO",
        },
        {
            "ocorrencia": "31/07/2023 17:32:00.000",
            "eventoId": "2000",
            "evento": "Faturado",
            "arCorreios": "",
            "frq": "ILG",
            "local": "SAO PAULO",
        },
    ]
    flash_api.organizar_datas(mock_dados)
    assert mock_dados[0]["ocorrencia"] == "31/07/2023 17:32:00.000"
    assert mock_dados[1]["ocorrencia"] == "30/07/2023 17:32:00.000"
    assert mock_dados[2]["ocorrencia"] == "26/07/2023 17:32:00.000"


@pytest.mark.dados_flash
# Teste para verificar se a função retorna dados válidos para um ID válido
def test_quando_buscar_id_valido_retornar_uma_lista():
    flash_api = FlashAPI()
    id_valido = 7909
    dados = flash_api.buscar_dados(id_valido)

    assert isinstance(dados, list)
    assert len(dados) > 0


@pytest.mark.dados_flash
# Teste para verificar se a função quando retornar o json, o último status estará formatado corretamente
def test_quando_retornar_lista_verificar_se_o_ultimo_status_esta_formatado_corretamente(
    flash_api,
):
    id_valido = 7909
    dados = flash_api.buscar_dados(id_valido)
    ultimo_status = dados[0]
    assert "ocorrencia" in ultimo_status
    assert "eventoId" in ultimo_status
    assert "evento" in ultimo_status
    assert "arCorreios" in ultimo_status
    assert "frq" in ultimo_status
    assert "local" in ultimo_status


@pytest.mark.dados_flash
# Teste para verificar se as chaves do último status possuem valores válidos
def test_quando_retornar_lista_verificar_se_as_chaves_possuem_valor_com_excecao_de_arCorreios(
    flash_api,
):
    id_valido = 7909
    dados = flash_api.buscar_dados(id_valido)
    ultimo_status = dados[0]
    assert ultimo_status["ocorrencia"] != ""
    assert ultimo_status["eventoId"] != ""
    assert ultimo_status["evento"] != ""
    assert ultimo_status["frq"] != ""
    assert ultimo_status["local"] != ""


@pytest.mark.dados_flash
# Teste para verificar se o "evento" do último status possui um valor dentro de SITUACOES
def test_quando_retornar_lista_verificar_se_o_evento_do_ultimo_status_possui_um_valor_dentro_de_SITUACOES(
    flash_api,
):
    id_valido = 7909
    dados = flash_api.buscar_dados(id_valido)
    ultimo_status = dados[0]
    assert ultimo_status["evento"] in SITUACOES.values()
