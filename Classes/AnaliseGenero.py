from Classes.Grafico import Grafico
import plotly.express as px
from sklearn.preprocessing import PolynomialFeatures #py -3.12 -m pip install scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import plotly.graph_objects as go
import pandas as pd

class AnaliseGenero(Grafico):
    def __init__(self, dataframe, firstValue: str, secondValue: str, colorValue: str, escolhaGrafico: str):
        super().__init__(dataframe, firstValue, secondValue, colorValue)
        self.escolhaGrafico = escolhaGrafico

    def criar_grafico(self):
        match self.escolhaGrafico:
            case "histogram":
                return px.histogram(self.dataframe, x=self.firstValue, y=self.secondValue, color=self.colorValue, 
                                    barmode='group', title='Quantidade de suicídios por gênero em cada período', 
                                    height=400, nbins=17, 
                                    color_discrete_sequence=px.colors.sequential.Rainbow).update_layout(yaxis_title="Quantidade").show()
                
            case "pie":
                return px.pie(self.dataframe, values=self.firstValue , names=self.secondValue, 
                              color=self.colorValue, title="Porcentagem de suicídios por gênero", hole=.4, 
                              color_discrete_sequence=px.colors.sequential.Rainbow).show()
            
            case _:
                print(f"Parâmetro escolhaGrafico inválido, escolha entre 'histogram' e 'pie'!")
                return

    #Modelo de regressão polinomial para prever suicídios por gênero em anos futuros             
    def modelo_regre_poli(self, grau_homens=2, grau_mulheres=2):
        # O dataframe tem as colunas: 'per_cod' (ano serial), 'gen_cod' (gênero), 'quantidade' (suicídios)
        df = self.dataframe

        # Transformação do 'per_cod' para o ano real (1989-2022)
        df['Período'] = df['per_cod'] + 1988

        # Separando os dados para Homens (gen_cod == 2) e Mulheres (gen_cod == 1)
        homens = df[df['gen_cod'] == 2]
        mulheres = df[df['gen_cod'] == 1]

        if len(homens) == 0 or len(mulheres) == 0:
            print("Erro: Não há dados suficientes para homens ou mulheres.")
            return

        # Dataframe Anos futuros
        anos_futuros = pd.DataFrame(np.arange(2023, 2031), columns=['Período'])

        # Regressão polinomial para homens
        poly_homens = PolynomialFeatures(degree=grau_homens)
        X_poly_homens = poly_homens.fit_transform(homens[['Período']])
        modelo_homens = LinearRegression()
        modelo_homens.fit(X_poly_homens, homens['Quantidade'])
        X_poly_futuros_homens = poly_homens.transform(anos_futuros)
        previsao_homens = modelo_homens.predict(X_poly_futuros_homens)
        erro_homens = np.std(homens['Quantidade'] - modelo_homens.predict(X_poly_homens))
        mse_homens = mean_squared_error(homens['Quantidade'], modelo_homens.predict(X_poly_homens))
        print("Modelo Polinomial - Homens")
        print(f"Previsão de suicídios (homens) 2023-2030: {previsao_homens}")
        print(f"Desvio padrão - Homens: {erro_homens}\n")

        # Regressão polinomial para mulheres
        poly_mulheres = PolynomialFeatures(degree=grau_mulheres)
        X_poly_mulheres = poly_mulheres.fit_transform(mulheres[['Período']])
        modelo_mulheres = LinearRegression()
        modelo_mulheres.fit(X_poly_mulheres, mulheres['Quantidade'])
        X_poly_futuros_mulheres = poly_mulheres.transform(anos_futuros)
        previsao_mulheres = modelo_mulheres.predict(X_poly_futuros_mulheres)
        erro_mulheres = np.std(mulheres['Quantidade'] - modelo_mulheres.predict(X_poly_mulheres))
        mse_mulheres = mean_squared_error(mulheres['Quantidade'], modelo_mulheres.predict(X_poly_mulheres))
        print("Modelo Polinomial - Mulheres")
        print(f"Previsão de suicídios (mulheres) 2023-2030: {previsao_mulheres}")
        print(f"Desvio padrão - Mulheres: {erro_mulheres}")

        fig = go.Figure()

        # Homens
        fig.add_trace(go.Scatter(x=homens['Período'], y=homens['Quantidade'],
                                mode='lines+markers', name="Homens (histórico)", line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=anos_futuros['Período'], y=previsao_homens,
                                mode='lines+markers', name="Homens (previsão)", line=dict(dash='dash', color='blue')))
        fig.add_trace(go.Scatter(x=anos_futuros['Período'], y=previsao_homens + erro_homens,
                                mode='lines', line=dict(color='blue', dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=anos_futuros['Período'], y=previsao_homens - erro_homens,
                                mode='lines', line=dict(color='blue', dash='dot'), showlegend=False))

        # Mulheres
        fig.add_trace(go.Scatter(x=mulheres['Período'], y=mulheres['Quantidade'],
                                mode='lines+markers', name="Mulheres (histórico)", line=dict(color='red')))
        fig.add_trace(go.Scatter(x=anos_futuros['Período'], y=previsao_mulheres,
                                mode='lines+markers', name="Mulheres (previsão)", line=dict(dash='dash', color='red')))
        fig.add_trace(go.Scatter(x=anos_futuros['Período'], y=previsao_mulheres + erro_mulheres,
                                mode='lines', line=dict(color='red', dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter(x=anos_futuros['Período'], y=previsao_mulheres - erro_mulheres,
                                mode='lines', line=dict(color='red', dash='dot'), showlegend=False))

        # Configurações do gráfico
        fig.update_layout(
            title="Previsão de Suicídios (1989-2030) - Regressão Polinomial",
            xaxis_title="Período",
            yaxis_title="Quantidade de Suicídios",
            template="plotly",
            legend_title="Gênero",
            hovermode="closest"
        )

        fig.show()