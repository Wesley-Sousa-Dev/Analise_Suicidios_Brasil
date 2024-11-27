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
                    query = "SELECT af.arm_cod, af.per_cod, af.quantidade_total, p.ano FROM arma_fogo af INNER JOIN periodo p ON p.per_cod = af.per_cod;"
                case 'gen_periodo':
                    query = "SELECT gp.gen_cod, gp.per_cod, gp.quantidade, g.tipo, g.descricao, p.ano, p.quantidade_total FROM gen_periodo gp INNER JOIN genero g ON g.gen_cod = gp.gen_cod INNER JOIN periodo p ON p.per_cod = gp.per_cod ORDER BY gp.per_cod, gp.gen_cod;"
                case 'reg_periodo':
                    query = "SELECT rp.per_cod, rp.reg_cod, rp.quantidade, r.nome, r.descricao, p.ano FROM reg_periodo rp INNER JOIN regiao r ON r.reg_cod = rp.reg_cod INNER JOIN periodo p ON p.per_cod = rp.per_cod ORDER BY rp.per_cod;"
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