import pytest
from app.database import ApiCnpj
from tests.test_insert_banco import TestClassInsertBanco
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
class TestClassDataBase:
    #O PEDAÇO DO CÓDIGO ESTA AQUI POIS NÃO CONSEGUE PEGAR CONEXÃO DO BANCO
    def test_para_verificar_se_lista_usuarios_esta_conseguindo_ser_alimentada_por_uma_lista(self):
        teste = [('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '3874'),('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '7010')]
        
        esperado = [{'nome': 'LUIS CARLOS DE FREITAS SERTAOZINHO', 'documento': '96163100000108', 'pedido': '3874'},
                    {'nome': 'LUIS CARLOS DE FREITAS SERTAOZINHO', 'documento': '96163100000108', 'pedido': '7010'}
                    ]
        lista_usuarios = []
        for user_data in teste:
                lista_usuarios.append(
                    {
                        "nome": user_data[0],
                        "documento": user_data[1],
                        "pedido": user_data[2],
                    }
                )
                
        assert lista_usuarios == esperado
        
    def test_para_saber_se_o_metodo_busca_cnpj_esta_retornando_uma_lista(self):
        esperado = [('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '3874'),('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '7010')]
        
        conn = psycopg2.connect(
                dbname=os.getenv('PROD_DB_INT_NAME'),
                user=os.getenv('PROD_DB_INT_USER'),
                password=os.getenv('PROD_DB_INT_PASS'),
                host=os.getenv('PROD_DB_INT_HOST'),
                port=5432,
            )

        query = f"""select nome, documento, pedido_1 from credenciamento.dashboard_rastreio_flash where documento = '{'96163100000108'}';"""

        cursor = conn.cursor()
        cursor.execute(query)

        records = cursor.fetchall()
        cursor.close()
        assert records == esperado
        
    def test_para_retornar_excpetion_IndexError_caso_no_metodo_retorna_lista_pedido_o_valor_de_user_data_0_faltar_um_indice(self):
        with pytest.raises(IndexError):
                teste = [('96163100000108', '3874'),('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '7010')]
                
                lista_usuarios = []
                for user_data in teste:
                        lista_usuarios.append(
                            {
                                "nome": user_data[0],
                                "documento": user_data[1],
                                "pedido": user_data[2],
                            }
                        )
                        
    def test_para_retornar_excpetion_ValueError_caso_no_metodo_retorna_lista_pedido_o_valor_de_user_data_0_estiver_vazio(self):
        with pytest.raises(ValueError):
            teste = [('', '96163100000108', '3874'), ('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '7010')]

            lista_usuarios = []
            for user_data in teste:
                if any(not item for item in user_data):
                    raise ValueError("Um item está com a string vazia")
                lista_usuarios.append(
                    {
                        "nome": user_data[0],
                        "documento": user_data[1],
                        "pedido": user_data[2],
                    }
                )

    def test_para_retornar_excpetion_ValueError_caso_no_metodo_retorna_lista_pedido_o_valor_de_user_data_1_estiver_como_inteiro(self):
        with pytest.raises(ValueError):
            teste = [('', 96163100000108, '3874'), ('LUIS CARLOS DE FREITAS SERTAOZINHO', '96163100000108', '7010')]

            lista_usuarios = []
            for user_data in teste:
                if isinstance(user_data[1], int):
                    raise ValueError("Documento é um inteiro")
                lista_usuarios.append(
                    {
                        "nome": user_data[0],
                        "documento": user_data[1],
                        "pedido": user_data[2],
                    }
                )

            
            
            
    