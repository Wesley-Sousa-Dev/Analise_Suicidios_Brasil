import psycopg2 as psy
import pandas as pd

class BancoDados:
    def __init__(self, dbname, user, password, host, port):
        try:
            self.db_connect = psy.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Conexão bem-sucedida!")
        except Exception as e:
            print(f"Erro ao conectar: {e}")
        
    def encerrar(self):
        try:
            self.db_connect.close()
        except Exception as e:
            return f"Erro ao encerrar a conexão: {e}"

