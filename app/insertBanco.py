import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from tqdm import tqdm

from app.baixaArquivo import extraiArquivo
from app.config import settings



class DataBase:
    def __init__(self) -> None:
        pass
        
    def criar_conexao(self):
        self.conn = psycopg2.connect(
                dbname=settings.DB_INT_NAME,
                user=settings.DB_INT_USER,
                password=settings.DB_INT_PASS,
                host=settings.DB_INT_HOST,
                port=5432,
            )
        return self.conn

    def criar_data_frame(self):
        try:
            
            arquivo = extraiArquivo()
            arquivo_path = f"./excel/{arquivo[0]}"
            if not os.path.exists(arquivo_path):
                raise FileNotFoundError(f"O arquivo {arquivo_path} não foi encontrado.")
            
            path = pd.read_csv(arquivo_path, sep=";")
            df = pd.DataFrame(path)
            return df.to_numpy()
        
        except FileNotFoundError as e:
            raise Exception(f"Não foi possível criar o DataFrame: {e}")
        
    def coleta_dados_banco(self, dados):
        for values in tqdm(dados):
            yield values

    def executa_query(self):
        conn = self.criar_conexao()
        cursor = conn.cursor()
        try:
            for values in self.coleta_dados_banco(self.criar_data_frame()):
                query = (
                    f"INSERT INTO credenciamento.dashboard_rastreio_flash(pedido_1, nome, documento) "
                    f"VALUES('{values[2]}','{values[5]}','{values[6]}')"
                )
                cursor.execute(query)
            conn.commit()
            
        except Exception as e:
            print(f"Erro durante a execução da query: {e}")
            
        finally:
            cursor.close()
            conn.close()
            

    def exclui_excel(self, diretorio):
        if os.path.exists(diretorio):
            for i in os.listdir(diretorio):
                os.remove(os.path.join(diretorio, i))

    def insert_banco(self):
        try:
            self.executa_query()
            
        except psycopg2.DatabaseError as e:
            print(f"Ocorreu um erro ao conectar ou interagir com o banco de dados: {e}")
            
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            
        finally:
            print("INSERT CONCLUÍDO!")
            diretorio = "./excel"
            self.exclui_excel(diretorio)


if __name__ == "__main__":
    banco = DataBase()
    banco.insert_banco()
