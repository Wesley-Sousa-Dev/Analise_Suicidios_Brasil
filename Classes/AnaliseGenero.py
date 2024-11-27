from Classes.Grafico import Grafico
import plotly.express as px


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
                