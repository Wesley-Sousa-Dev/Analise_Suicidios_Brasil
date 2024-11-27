from Classes.Grafico import Grafico
import plotly.express as px
import pandas as pd
import numpy as np

class AnaliseRegiao(Grafico):
    def __init__(self, dataframe, firstValue: str, secondValue: str, colorValue: str):
        super().__init__(dataframe, firstValue, secondValue, colorValue)

    def criar_grafico(self):
        return px.line(self.dataframe, x = self.firstValue, y = self.secondValue, color = self.colorValue, 
                       title = 'Suicídios em cada região por período', markers = True, 
                       color_discrete_sequence = px.colors.qualitative.G10).show()
    
    def anos_max_min(self):
        #O que o dataframe terá:
        #'Período', 'Quantidade', 'Descrição
        df = self.dataframe
        anos = df[(df['Período'] >= 2013) & (df['Período'] <= 2022)]
        #dados = []



        # Criar dados aleatórios para cada ano e região
        #for ano in anos['Período'].unique():
         #   for regiao in df['Descrição'].unique():
          #      valor = np.random.randint(1000, 5000)  # Valor aleatório entre 1000 e 5000
           #     dados.append({'Descrição': regiao, 'Período': ano, 'Quantidade': valor})

        #df = pd.DataFrame(dados)

        # Encontrar o maior e menor valor para cada região com seu respectivo ano
        resultados = []

        for regiao in df['Descrição'].unique():
            # Filtrar os dados da região
            dados_regiao = df[df['Descrição'] == regiao]

            # Maior valor
            max_valor = dados_regiao['Quantidade'].max()
            ano_max = dados_regiao[dados_regiao['Quantidade'] == max_valor]['Período'].values[0]

            # Menor valor
            min_valor = dados_regiao['Quantidade'].min()
            ano_min = dados_regiao[dados_regiao['Quantidade'] == min_valor]['Período'].values[0]

            resultados.append({'Descrição': regiao, 'Ano_Maior': ano_max, 'Maior_Valor': max_valor, 
                            'Ano_Menor': ano_min, 'Menor_Valor': min_valor})

        # Transformar os resultados em um DataFrame
        df_resultados = pd.DataFrame(resultados)

        print("Resultados (Maior e Menor Valor por Região):")
        print(df_resultados)