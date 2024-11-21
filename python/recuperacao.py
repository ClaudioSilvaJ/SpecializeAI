from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from sentence_transformers import SentenceTransformer, util


df = pd.read_csv('assets/datasets/sintomas_variacoes.csv')
documentos = df.values.flatten().tolist()
documentos = [str(x) for x in documentos if str(x) != 'nan']

# vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(documentos)
# entrada = vectorizer.transform(["Dor na cabeça"])
# similaridade = cosine_similarity(entrada, X)
# print("Similaridades:", similaridade[0])
# print(similaridade)
# indice_mais_semelhante = similaridade[0].argmax()
# print("Documento mais semelhante:", documentos[indice_mais_semelhante])

class Recuperacao:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.sentence = SentenceTransformer('all-MiniLM-L6-v2')
        self.X = self.vectorizer.fit_transform(documentos)

    def recuperar(self, consulta):
        print("Consulta:", consulta)
        entrada = self.vectorizer.transform([consulta])
        similaridade = cosine_similarity(entrada, self.X)
        indice_mais_semelhante = similaridade[0].argmax()
        print("Documento mais semelhante:", documentos[indice_mais_semelhante])
        return documentos[indice_mais_semelhante]
    
    def recuperar_sentence(self, consulta):
        embeddings_documentos = self.sentence.encode(documentos, convert_to_tensor=True)
        embedding_consulta = self.sentence.encode(consulta, convert_to_tensor=True)
        similaridade = util.cos_sim(embedding_consulta, embeddings_documentos)
        indice_mais_semelhante = similaridade.argmax()
        print("Documento mais semelhante:", documentos[indice_mais_semelhante])
        return documentos[indice_mais_semelhante]

