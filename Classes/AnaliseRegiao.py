from Classes.Grafico import Grafico
import plotly.express as px
import pandas as pd
import numpy as np

class AnaliseRegiao(Grafico):
    def __init__(self, dataframe, firstValue: str, secondValue: str, colorValue: str):
        super().__init__(dataframe, firstValue, secondValue, colorValue)

    def criar_grafico(self):
        return px.line(self.dataframe, x = self.firstValue, y = self.secondValue, color = self.colorValue, 
                       title = 'Quantidade de suicídios por região em cada período', markers = True, 
                       color_discrete_sequence = px.colors.qualitative.G10).show()
    
    #Verificar qual o ano com a maior e o ano com a menor quantidade de suicídios de cada região nos últimos 10 anos
    def anos_max_min(self):
        #O que o DataFrame terá:
        #'Período', 'Quantidade', 'Descrição
        df = self.dataframe
        df = df[(df['Período'] >= 2013) & (df['Período'] <= 2022)]
        resultados = []

        for regiao in df['Descrição'].unique():
            dados_regiao = df[df['Descrição'] == regiao]

            # Maior valor
            max_valor = dados_regiao['Quantidade'].max()
            ano_max = dados_regiao[dados_regiao['Quantidade'] == max_valor]['Período'].values[0]

            # Menor valor
            min_valor = dados_regiao['Quantidade'].min()
            ano_min = dados_regiao[dados_regiao['Quantidade'] == min_valor]['Período'].values[0]

            resultados.append({'Descrição': regiao, 'Ano_Maior': ano_max, 'Maior_Valor': max_valor, 
                            'Ano_Menor': ano_min, 'Menor_Valor': min_valor})

        df_resultados = pd.DataFrame(resultados)

        print("Resultados (Ano_Maior e Ano_Menor por Região nos últimos 10 anos):")
        print(df_resultados)