import os

import pytest
import selenium.common.exceptions as WebDriverException

from app.baixaArquivo import ArquivoExcel, extraiArquivo


@pytest.fixture(scope="module")
def arquivo_excel():
    return ArquivoExcel()


@pytest.fixture(scope="module")
def download_dir(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp("temp_excel")
    return temp_dir.strpath


@pytest.mark.baixar_arquivo
def test_quando_funcao_acessarPaginaLogar_for_chamada_verificar_se_ela_abre_a_pagina_da_api_e_faz_o_login(
    arquivo_excel,
):
    arquivo_excel.acessarPaginaLogar(
        "https://phoenix.jall.com.br/FlashPhoenix/pages/_defaultPages/empty-page.xhtml"
    )
    assert "FLASH PHOENIX" in arquivo_excel.driver.title


@pytest.mark.baixar_arquivo
def test_quando_funcao_acessarPaginaDownloadBaixar_for_chamada_verificar_se_ela_abre_abre_a_pagina_do_picking():
    arquivo_excel = ArquivoExcel()
    arquivo_excel.acessarPaginaLogar(
        "https://phoenix.jall.com.br/FlashPhoenix/pages/_defaultPages/empty-page.xhtml"
    )

    arquivo_excel.acessarPaginaDownloadBaixarZip(
        "https://phoenix.jall.com.br/FlashPhoenix/pages/relatorios/relatorioPicking.xhtml",
        baixar=False,
    )
    assert "relatorioPicking" in arquivo_excel.driver.current_url


@pytest.mark.baixar_arquivo
def test_para_verificar_se_a_funcao_baixarArquivo_baixa_o_arquivo_corretamente():
    arquivo_excel = ArquivoExcel()
    arquivo_excel.baixarArquivo()
    assert "RELATORIO_PICKING_GERAL_" in arquivo_excel.nome_arquivo_zip


@pytest.mark.baixar_arquivo
def test_para_verificar_se_ao_chamar_extrairArquivo_sao_gerados_dois_arquivos_novos():
    arquivo_excel = ArquivoExcel()
    diretorio = os.path.join(os.getcwd(), "excel")
    tamanho_atual = len(os.listdir(diretorio))
    arquivo_excel.extrairArquivoZip()
    tamanho_final = len(os.listdir(diretorio))
    assert tamanho_final == tamanho_atual + 2


@pytest.mark.baixar_arquivo
def test_quando_funcao_removerZip_chamada_ela_adiciona_um_arquivo_zip_extrai_ele_e_remove():
    arquivo_excel = ArquivoExcel()
    diretorio = os.path.join(os.getcwd(), "excel")
    tamanho_atual = len(os.listdir(diretorio))
    arquivo_excel.removerZip()
    tamanho_final = len(os.listdir(diretorio))
    assert tamanho_final == tamanho_atual + 1


@pytest.mark.baixar_arquivo
def test_verificar_se_extraiArquivo_gera_um_arquivo_excel_valido():
    excel_files = extraiArquivo()
    assert excel_files != None


@pytest.mark.baixar_arquivo
def test_verifica_se_acessarPaginaLogar_retorna_o_erro_com_endereco_invalido():
    arquivo_excel = ArquivoExcel()

    assert (
        "ocorreu um erro na função acessarPaginaLogar()"
        in arquivo_excel.acessarPaginaLogar("https://pagina-que-nao-existe.com")
    )


@pytest.mark.baixar_arquivo
def test_verificar_se_acessarPaginaDownloadBaixar_retorna_erro_com_pagina_invalida():
    arquivo_excel = ArquivoExcel()
    arquivo_excel.acessarPaginaLogar(
        "https://phoenix.jall.com.br/FlashPhoenix/pages/_defaultPages/empty-page.xhtml"
    )
    assert (
        "ocorreu um erro na função acessarPaginaDownloadBaixarZip()"
        in arquivo_excel.acessarPaginaDownloadBaixarZip(
            "https://pagina-que-nao-existe.com",
            baixar=False,
        )
    )
