
import pickle
import pandas as pd
import numpy as np

class LogisticModel():
    def __init__(self,model_file='assets/model/modelo_logistico_traduzido.pkl', weight_file='assets/datasets/Sintomas_pesos.csv', prediction_number=3):
        self.__df = pd.DataFrame(columns=self.__load_symptoms(weight_file))
        self.__pesos_df = self.__load_weights(weight_file)
        self.predictions_number = prediction_number
        self.model = self.__load_model(model_file)

    def __load_symptoms(self, symptoms_file):
        try:
            symptoms_df = pd.read_csv(symptoms_file)
            return symptoms_df['Sintoma'].tolist()
        except FileNotFoundError:
            print(f"Erro: Arquivo {symptoms_file} não encontrado.")
            return []

    def __load_model(self, model_file):
        try:
            with open(model_file, 'rb') as file:
                model = pickle.load(file)
            return model
        except FileNotFoundError:
            print(f"Erro: Arquivo {model_file} não encontrado.")
            return None
    
    def __load_weights(self, weight_file):
        try:
            pesos_df = pd.read_csv(weight_file)
            return pesos_df
        except FileNotFoundError:
            print(f"Erro: Arquivo {weight_file} não encontrado.")
            return pd.DataFrame()
        
    def __create_symptom_line(self, symptoms):
        linha_sintomas = [0] * len(self.__df.columns)
        self.__df.columns = self.__df.columns.str.strip()

        pesos_dict = dict(zip(self.__pesos_df['Sintoma'].str.strip(), self.__pesos_df['Peso']))

        for sintoma in symptoms:
            if sintoma in self.__df.columns:
                index = self.__df.columns.get_loc(sintoma)
                print(pesos_dict.get(sintoma, 1))
                print(linha_sintomas[index])
                linha_sintomas[index] = 1 * pesos_dict.get(sintoma, 1)
        
        return linha_sintomas

    def __interpret_results(self, predictions):
        indices = np.argsort(predictions[0])[(-1)*self.predictions_number:][::-1]
        possibilidades = self.model.classes_
        return [possibilidades[i] for i in indices]

    def predict(self, symptoms):
        linha_sintomas = self.__create_symptom_line(symptoms)

        self.__df.loc[len(self.__df)] = linha_sintomas
        predictions = self.model.predict_proba(self.__df.iloc[-1].values.reshape(1, -1))

        return self.__interpret_results(predictions)