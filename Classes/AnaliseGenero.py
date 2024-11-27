from Classes.Grafico import Grafico
import plotly.express as px
from sklearn.preprocessing import PolynomialFeatures #py -3.12 -m pip install scikit-learn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

class AnaliseGenero(Grafico):
    def __init__(self, dataframe, firstValue: str, secondValue: str, colorValue: str, escolhaGrafico: str):
        super().__init__(dataframe, firstValue, secondValue, colorValue)
        self.escolhaGrafico = escolhaGrafico

    def criar_grafico(self):
        match self.escolhaGrafico:
            case "histogram":
                return px.histogram(self.dataframe, x=self.firstValue, y=self.secondValue, color=self.colorValue, 
                                    barmode='group', title='Suicídios de gênero por período', height=400, nbins=17, 
                                    color_discrete_sequence=px.colors.sequential.Rainbow).update_layout(yaxis_title="Quantidade").show()
                
            case "pie":
                return px.pie(self.dataframe, values=self.firstValue , names=self.secondValue, 
                              color=self.colorValue, title="Porcentagem de suicídios por gênero", hole=.4, 
                              color_discrete_sequence=px.colors.sequential.Rainbow).show()
            
            case _:
                print(f"Parâmetro escolhaGrafico inválido, escolha entre 'histogram' e 'pie'!")
                return
                
    def modelo_regre_poli(self):
        # O dataframe tem as colunas: 'per_cod' (ano), 'gen_cod' (gênero), 'quantidade' (suicídios)
        df = self.dataframe
    
        # Transformação do 'per_cod' para o ano real (1989-2022)
        df['ano'] = df['per_cod'] + 1988
        
        # Verificando os dados do dataframe
        print("DataFrame com anos transformados:")
        print(df.head())  # Verifique as primeiras linhas para garantir que os dados estão corretos
        
        # Filtrando dados para o período entre 2013 e 2022
        anos = df[(df['ano'] >= 2013) & (df['ano'] <= 2022)]
        
        # Verificando se a filtragem foi bem-sucedida
        print("\nDados filtrados entre 2013 e 2022:")
        print(anos.head())
        
        # Separando os dados para Homens (gen_cod == 2) e Mulheres (gen_cod == 1)
        homens = anos[anos['gen_cod'] == 2]
        mulheres = anos[anos['gen_cod'] == 1]
        
        # Verificando os dados de homens e mulheres
        print("\nDados de Homens (gen_cod == 2):")
        print(homens.head())
        print("\nDados de Mulheres (gen_cod == 1):")
        print(mulheres.head())
        
        # Garantir que existem dados para cada gênero
        if len(homens) == 0 or len(mulheres) == 0:
            print("Erro: Não há dados suficientes para homens ou mulheres.")
            return

        # Criando o transformador de características polinomiais
        grau = 2  # Ajuste o grau do polinômio conforme necessário
        poly = PolynomialFeatures(degree=grau)
        
        # Transformando os dados para o modelo polinomial
        X_poly_homens = poly.fit_transform(homens[['ano']])
        X_poly_mulheres = poly.fit_transform(mulheres[['ano']])
        
        # Criando e treinando os modelos
        modelo_homens = LinearRegression()
        modelo_homens.fit(X_poly_homens, homens['quantidade'])
        
        modelo_mulheres = LinearRegression()
        modelo_mulheres.fit(X_poly_mulheres, mulheres['quantidade'])
        
        # Fazendo previsões para os anos futuros (2023-2030)
        anos_futuros = np.arange(2023, 2031).reshape(-1, 1)
        X_poly_futuros = poly.transform(anos_futuros)
        
        previsao_homens = modelo_homens.predict(X_poly_futuros)
        previsao_mulheres = modelo_mulheres.predict(X_poly_futuros)
        
        # Avaliação do modelo com MSE
        mse_homens = mean_squared_error(homens['quantidade'], modelo_homens.predict(X_poly_homens))
        mse_mulheres = mean_squared_error(mulheres['quantidade'], modelo_mulheres.predict(X_poly_mulheres))
        
        # Resultados
        print("Modelo Polinomial - Homens")
        print(f"Erro Quadrático Médio (MSE): {mse_homens}")
        print(f"Previsão de suicídios (homens) 2023-2030: {previsao_homens}\n")
        
        print("Modelo Polinomial - Mulheres")
        print(f"Erro Quadrático Médio (MSE): {mse_mulheres}")
        print(f"Previsão de suicídios (mulheres) 2023-2030: {previsao_mulheres}")
        
        # Visualização
        plt.figure(figsize=(10, 6))
        
        # Homens
        if len(homens) > 0:
            plt.plot(homens['ano'], homens['quantidade'], 'o-', label="Homens (histórico)")
            plt.plot(anos_futuros, previsao_homens, 'o--', label="Homens (previsão)")
        
        # Mulheres
        if len(mulheres) > 0:
            plt.plot(mulheres['ano'], mulheres['quantidade'], 'o-', label="Mulheres (histórico)")
            plt.plot(anos_futuros, previsao_mulheres, 'o--', label="Mulheres (previsão)")
        
        # Configurações do gráfico
        plt.title("Previsão de Suicídios (2023-2030) - Regressão Polinomial")
        plt.xlabel("Ano")
        plt.ylabel("Quantidade de Suicídios")
        plt.legend()
        plt.grid()
        plt.show()