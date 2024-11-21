import pandas as pd
class ArquivoInspecao:    
    def __init__(self, caminho):
        self.eUmCSV = self.ArquivoValido(caminho)
        if self.eUmCSV:
            self.dataframe = pd.read_csv(caminho, sep=";")
            self.cabecalho = self.dataframe.head()
            self.verifica = not self.dataframe.isna().values.any() and not self.cabecalho.empty
        else:
            raise Exception(e)
        
    def ArquivoValido(self, caminho):
        with open(caminho, "r") as file:
            return caminho.lower().endswith('.csv')