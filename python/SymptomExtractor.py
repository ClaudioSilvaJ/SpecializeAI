import pandas as pd
import re
import unicodedata

class SymptomExtractor:
    def __init__(self, dataset_path):
        self.df = pd.read_csv(dataset_path)
    
    @staticmethod
    def remover_acentos(texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'
        )

    def buscar_referencias(self, texto):
        referencias_encontradas = []
        texto_normalizado = self.remover_acentos(texto.lower())
        
        for _, row in self.df.iterrows():
            referencia = row['referencia']
            referencia_normalizada = self.remover_acentos(referencia.lower())
            variacoes = row.drop('referencia').dropna().str.lower().apply(self.remover_acentos).tolist()

            todas_variacoes = [referencia_normalizada] + variacoes
            regex = '|'.join(map(re.escape, todas_variacoes))

            if re.search(regex, texto_normalizado):
                referencias_encontradas.append(referencia)
        
        return referencias_encontradas

