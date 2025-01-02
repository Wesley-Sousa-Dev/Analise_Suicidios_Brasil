import pandas as pd

class Arquivo:
    def __init__(self, caminho):
        self.eUmCSV = self.arquivo_valido(caminho)
        if self.eUmCSV:
            self.dataframe = pd.read_csv(caminho, sep=";")
            self.cabecalho = self.dataframe.head()
            self.verifica = (
                not self.dataframe.isna().values.any() and not self.cabecalho.empty
            )
        else:
            raise Exception(f"O arquivo {caminho.split("/")[-1]} não é um CSV!")

    def arquivo_valido(self, caminho):
        return caminho.lower().endswith(".csv")
