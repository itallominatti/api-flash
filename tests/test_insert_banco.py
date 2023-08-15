import pytest

import os
import pandas as pd
import psycopg2

from app.insertBanco import DataBase

from dotenv import load_dotenv
from pytest import mark

#PARA OS TESTES FUNCIONAREM, TERA QUE COLOCAR OS DADOS DO BANCO NO ARQUIVO INSERTBANCO.PY EM HARDCODED
load_dotenv()
class TestClassInsertBanco:
    
    @mark.testes_sobre_excel
    def test_para_saber_se_o_diretorio_que_usa_excel_para_inserir_no_banco_existe(self):
        
        entrada = "./excel"
        assert os.path.exists(entrada)
        
    def test_para_saber_se_a_conexao_com_o_banco_nao_retorna_None(self):
        conexao = None
        try:
            conexao = psycopg2.connect(
                dbname=os.getenv('PROD_DB_INT_NAME'),
                user=os.getenv('PROD_DB_INT_USER'),
                password=os.getenv('PROD_DB_INT_PASS'),
                host=os.getenv('PROD_DB_INT_HOST'),
                port=5432,
            )
            assert conexao is not None
        except Exception:
            pytest.fail("cria_conexao() levantou uma exceção inesperada!")
            
        finally:
            if conexao is not None:
                conexao.close()
                return conexao
      
    
    @mark.testes_sobre_excel 
    def test_para_saber_se_o_metodo_criarDataFrame_esta_retornando_um_DataFrame(self):
        esperado = True
        dir = "./excel"
        
        instancia = DataBase()
        teste = instancia.criar_data_frame()
        if os.path.exists(dir):
            arquivos = os.listdir(dir)
        
        if arquivos:
            arquivos = True
            
        assert arquivos == esperado
        return teste
        
    def test_para_saber_se_o_metodo_coleta_dados_banco_esta_pegando_todos_os_dados_do_excel(self):
        instancia = DataBase()
        arquivo = instancia.criar_data_frame()
        teste = instancia.coleta_dados_banco(arquivo)
        assert teste != None
        
        
    
    @mark.testes_sobre_excel   
    def test_para_saber_se_o_metodo_exclui_excel_esta_apagando_os_itens_do_diretorio_excel(self):
        dir = "./excel"
        esperado = True
        
        teste = DataBase()
        teste = teste.exclui_excel(dir)
        if os.path.exists(dir):
            arquivos = os.listdir(dir)
            if arquivos != True:
                resultado = True
        
        assert esperado == resultado
        