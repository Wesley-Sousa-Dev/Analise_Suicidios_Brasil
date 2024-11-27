from Classes.Grafico import Grafico
import plotly.express as px

class AnaliseArmaFogo(Grafico):
    def __init__(self, dataframe, firstValue: str, secondValue: str, colorValue: str):
        super().__init__(dataframe, firstValue, secondValue, colorValue)

    def criar_grafico(self):
        return px.scatter(self.dataframe, x = self.firstValue, y = self.secondValue, color = self.colorValue, 
                          title = 'Suicídios por arma de fogo em cada período', size = "size_scaled", 
                          hover_name = self.firstValue, log_x = True, size_max = 50, 
                          color_continuous_scale = px.colors.sequential.Rainbow_r).show()