import pandas as pd
from Classes.BancoDados import BancoDados

class BancoDML(BancoDados):
    def __init__(self, dbname, user, password, host, port):
        super().__init__(dbname, user, password, host, port)
 
    def inserir_total(self, suicidioDf):
        try:
            suicidioDf = suicidioDf.rename(columns={'período': 'ano', 'valor': 'quantidade_total'})

            dados = suicidioDf[['ano', 'quantidade_total']].to_records(index=False).tolist()
            
            query = """
            INSERT INTO periodo (ano, quantidade_total)
            VALUES (%s, %s);
            """

            with self.db_connect.cursor() as cursor:
                cursor.executemany(query, dados)

            self.db_connect.commit()
            return "Dados inseridos com sucesso!"
        
        except Exception as e:
            self.db_connect.rollback()
            return f"Erro ao inserir os dados: {e}"

    def inserir_gen(self, homemDf, mulherDf, colunasPer):
        try:
            dadosMulher = mulherDf.rename(columns={'período':'ano', 'valor': 'quantidade'}, inplace=True)
            dadosMulher = mulherDf.merge(colunasPer, on='ano', how='left')
            dadosMulher['gen_cod'] = 1
            
            dadosHomem = homemDf.rename(columns={'período':'ano', 'valor':'quantidade'}, inplace=True)
            dadosHomem = homemDf.merge(colunasPer, on='ano', how='left')
            dadosHomem['gen_cod'] = 2

            #print(f"Dados DF mulher pós merge: \n{dadosMulher} \n\nDados DF homem pós merge: \n{dadosHomem}")

            dados = pd.concat([dadosMulher, dadosHomem])
            #print(f"\n\nDataframe concatenado: \n{dados}")

            dados = dados[['per_cod', 'gen_cod','quantidade']].to_records(index=False).tolist()
            
            query = """
            INSERT INTO gen_periodo (per_cod, gen_cod, quantidade)
            VALUES (%s, %s, %s);
            """

            with self.db_connect.cursor() as cursor:
                cursor.executemany(query, dados)

            self.db_connect.commit()
            return "Dados inseridos com sucesso!"
        
        except Exception as e:
            self.db_connect.rollback()
            return f"Erro ao inserir os dados: {e}"
        
    def inserir_reg(self, colunasReg, regiaoDf, colunasPer):
        #O que esperasse ter em cada parâmetro passado:
        #colunasReg: ['reg_cod', 'nome']
        #regiaoDf: ['nome', 'período', 'valor']
        #colunasPer: ['per_cod', 'ano']

        try:
            dadosReg = regiaoDf.copy()
            dadosReg = dadosReg.rename(columns={'período':'ano', 'valor':'quantidade'})
            dadosReg = dadosReg.merge(colunasReg, on='nome', how='left')
            dadosReg = dadosReg.merge(colunasPer, on='ano', how='left')

            dadosReg = dadosReg[['per_cod', 'reg_cod','quantidade']].to_records(index=False).tolist()
            
            query = """
            INSERT INTO reg_periodo (per_cod, reg_cod, quantidade)
            VALUES (%s, %s, %s);
            """

            with self.db_connect.cursor() as cursor:
                cursor.executemany(query, dadosReg)

            self.db_connect.commit()
            return "Dados inseridos com sucesso!"

        except Exception as e:
            self.db_connect.rollback()
            return f"Erro ao inserir os dados: {e}"

    def inserir_dados_fogo(self, mulherFogoDf, homemFogoDf, colunasPer):
        #O que esperasse ter em cada parâmetro passado:
        #mulherFogoDf: ['período', 'valor']
        #homemFogoDf: ['período', 'valor']
        #colunasPer: ['per_cod', 'ano']

        try:
            dadosFog = mulherFogoDf.copy()

            #Explicação rápida: suffixes evita conflitos de colunas com nomes duplicados adicionando um sufixo em ambos
            #em outras palavras valor mulherFogoDf vira: valor_mulher e o do merge do homemFogo Df é inserido como: valor_homem
            dadosFog = dadosFog.merge(homemFogoDf, on='período', how='left', suffixes=('_mulher', '_homem'))
            
            dadosFog['quantidade_total'] = dadosFog['valor_mulher'] + dadosFog['valor_homem']
            dadosFog = dadosFog.rename(columns={'período':'ano'})
            dadosFog = dadosFog.merge(colunasPer, on='ano', how='left')

            dadosFog = dadosFog[['per_cod', 'quantidade_total']].to_records(index=False).tolist()

            query = """
            INSERT INTO arma_fogo (per_cod, quantidade_total)
            VALUES (%s, %s);
            """

            with self.db_connect.cursor() as cursor:
                cursor.executemany(query, dadosFog)

            self.db_connect.commit()
            return "Dados inseridos com sucesso!"

        except Exception as e:
            self.db_connect.rollback()
            return f"Erro ao inserir os dados: {e}"