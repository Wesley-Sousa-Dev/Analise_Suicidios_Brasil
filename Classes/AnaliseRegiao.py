from Classes.Grafico import Grafico
import plotly.express as px

class AnaliseRegiao(Grafico):
    def __init__(self, dataframe, firstValue: str, secondValue: str, colorValue: str):
        super().__init__(dataframe, firstValue, secondValue, colorValue)

    def criar_grafico(self):
        return px.line(self.dataframe, x = self.firstValue, y = self.secondValue, color = self.colorValue, title = 'Suicídios em cada região por período', markers = True, color_discrete_sequence = px.colors.qualitative.G10)