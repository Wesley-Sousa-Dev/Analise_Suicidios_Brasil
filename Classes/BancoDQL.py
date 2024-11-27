import psycopg2 as psy
import pandas as pd
from Classes.BancoDados import BancoDados

class BancoDQL(BancoDados):
    def __init__(self, dbname, user, password, host, port):
        super().__init__(dbname, user, password, host, port)

    def buscar_dados(self, chosentable):
        try:
            self.db_connect.rollback()

            match chosentable:
                case 'periodo':
                    query = "SELECT * FROM periodo ORDER BY ano;"
                case 'genero':
                    query = "SELECT * FROM genero;"
                case 'regiao':
                    query = "SELECT * FROM regiao;"
                case 'arma_fogo':
                    query = "SELECT * FROM arma_fogo;"
                case 'gen_periodo':
                    query = "SELECT * FROM gen_periodo ORDER BY per_cod;"
                case 'reg_periodo':
                    query = "SELECT * FROM reg_periodo ORDER BY per_cod;"
                case _:
                    return "Table escolhida não existe."


            with self.db_connect.cursor() as cursor:
                cursor.execute(query)
                resultados = cursor.fetchall()
                colunas = [desc[0] for desc in cursor.description]
        
            dataframe = pd.DataFrame(resultados, columns=colunas)
            return dataframe 
        
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")