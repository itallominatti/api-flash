import psycopg2

from app.config import settings
from app.insertBanco import DataBase


class ApiCnpj(DataBase):
    
    def __init__(self) -> None:
        super().__init__()
        
    def busca_cnpj(self,cnpj) -> list:
        try:
            conn = self.criar_conexao()

            query = f"""select nome, documento, pedido_1 from
            {settings.DB_INT_NAME}.credenciamento.dashboard_rastreio_flash where documento = '{cnpj}';"""

            cursor = conn.cursor()
            cursor.execute(query)

            self.records = cursor.fetchall()
            cursor.close()
            return self.records
        
        except psycopg2.Error:
            print("esse CNPJ não foi localizado na base")
            return
        
    def retorna_lista_de_pedidos(self,cnpj) -> list:
        try:
            lista_usuarios = []
            for user_data in self.busca_cnpj(cnpj):
                if any(not item for item in user_data):
                    raise ValueError("Um item está com a string vazia")
                lista_usuarios.append(
                    {
                        "nome": user_data[0],
                        "documento": user_data[1],
                        "pedido": user_data[2],
                    }
                )
            return lista_usuarios
        except ValueError:
            raise(ValueError, "provavelmente um item está com a string vazia")
        except IndexError:
            raise(IndexError, "Provavelmente faltou um item na lista")
            



if __name__ == "__main__":
    teste = ApiCnpj()
    print(teste.retorna_lista_de_pedidos(96163100000108))
