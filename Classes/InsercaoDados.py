import psycopg2 as psy
import pandas as pd

class InsercaoDados:
#Homens arma de fogo e Mulheres arma de fogo

#Mulheres e homens suicídio e região

#Suicidio Total
    def inserir_total(self, bancoDados, suicidioDf):
        #Retirar cod e nome do dataframe, perido se torna ano e valor se torna quantidade_total
        try:
            suicidioDf = suicidioDf.drop(columns=['cod', 'nome'])
            conn = bancoDados.db_connect.set_session()
            suicidioDf.to_sql('periodo', con=conn, if_exists='append', index=False)
            conn.close()
        except Exception as e:
            return f"Erro ao inserir os dados: {e}"
                


    def inserir_arma_fogo(self, bancoDados, mulherDf, homemDf):
            #Juntar homem e mulher por periodo - quantidade total
            #Pegar per_cod do Periodo(tabela banco de dados) e substituir periodo por per_cod
            #Adicionar no banco de dados
            return




    def insercao_dados(self, bancoDados):
        cursor = bancoDados.db_connect.cursor()

        tables = {
            'periodo': ['ano', 'quantidade_total'],
            'genero': ['tipo', 'descricao'],
            'regiao': ['nome', 'descricao'],
            'gen_periodo': ['per_cod', 'gen_cod', 'quantidade'],
            'reg_periodo': ['per_cod', 'reg_cod', 'quantidade']
        }

        if chosenTable not in tables:
            print(f"Tabela {chosenTable} não encontrada. Verifique o nome.")
            return       
        
        table_columns = tables[chosenTable]

        placeholders = ', '.join(['%s'] * len(table_columns))
        columns = ', '.join(table_columns)
        insert_query = f"INSERT INTO {chosenTable} ({columns}) VALUES ({placeholders})"



        try:
            #Inserindo cada linha do DataFrame
            for _, row in dataframe.iterrows():
                values = tuple(row[col] for col in table_columns)
                cursor.execute(insert_query, values)

            self.db_connect.commit()
            print(f"Dados inseridos com sucesso na tabela {chosenTable}!")

        except Exception as e:
            self.db_connect.rollback()
            print(f"Erro ao inserir dados: {e}")

        finally:
            cursor.close()
            self.db_connect.close()
            return

