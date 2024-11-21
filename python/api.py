import ollama
from fastapi import FastAPI
from pydantic import BaseModel
from model import model
import pandas as pd
import re
import unicodedata
from recuperacao import Recuperacao


app = FastAPI()
recuperacao = Recuperacao()

class MessageRequest(BaseModel):
    message: str

@app.post("/extract-symptoms")
async def extract_symptoms(request: MessageRequest):
    message = request.message
    print(message)
    result = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': '''
            Chat, vou te dar uma lista de sintomas separados por vírgulas e todos em minúsculas. Nas próximas mensagens, vou entrar com mensagens rotineiras. Quero que você extraia e me retorne apenas os sintomas que estão exatamente na lista caso tenha um sintoma que é sinonimo ou parecido com um sintoma da lista pode inclui-lo porem com o nome que aparece na lista, ou seja, na mesma forma (singular, plural, gênero) e sem sinônimos. Se houver alguma variação gramatical, use a forma original da lista. Ao final, me retorne apenas uma lista com os sintomas da lista que apareceram, separados por vírgulas e em minúsculas. Caso não encontre nada, retorne apenas "nenhum". Se um sintoma não estiver listado, não cite ele. 
            Em caso de um dor em uma parte do corpo e essa dor não estiver na lista, inclua como Dor Muscular.
            Retorne apenas a lista de sintomas sem nenhum outro texto.
            Lista de sintomas: Coceira, comichão, prurido, curubas, erupção cutânea, vermelhidão, descamação, erupções nodulares na pele, prurido nodular, nódulos firmes, caroço na pele, manchas discromáticas, manchas claras, manchas escuras, mancha colorida, espirros contínuos, espirrando muito, espirros persistentes, calafrios, horripilação, tremor de frio, arrepios, tremedeira, calafrio leve, olhos lacrimejantes, lágrimas nos olhos, olhos molhados, dor de estômago, dor de barriga, desconforto gástrico, acidez, queimação, azia, úlceras na língua, afta, feridas na língua, vômito, ânsia de vômito, enjoo extremo, tosse, muita tosse, tosse intensa, dor no peito, aperto no peito, desconforto no tórax, pele amarelada, icterícia, amarelão, cor amarela na pele, náusea, ânsia, mal-estar estomacal, perda de apetite, perda de fome, falta de fome, dor abdominal, dor no abdômen, dor na barriga, amarelamento dos olhos, olhos amarelos, icterícia ocular, ardência ao urinar, dificuldade de urinar, desconforto urinário, manchas na urina, urina colorida, coloração alterada da urina, passagem de gases, sons no intestino, gases intestinais, coceira interna, incomodação nos órgãos, irritação interna, indigestão, má digestão, dispepsia, desperdício muscular, anemia, fraqueza muscular, manchas na garganta, hematomas na garganta, lesões na garganta, febre alta, calor excessivo, febre intensa, contatos extraconjugais, muita vontade de transar, virilidade, sexo, fadiga, cansaço, exaustão, esgotamento, fraqueza, perda de peso, definhar, desengordar, inquietação, perda de atenção, agitação, letargia, pouca energia, indolência, inércia, torpor, desinteresse, nível de açúcar irregular, glicemia alterada, glicose alterada, visão turva e distorcida, visão embaçada, visão desfocada, obesidade, gordo, excesso de peso, corpulência, adiposidade, fome excessiva, apetite elevado, muita fome, aumento de apetite, muito apetite, poliúria (urina excessiva), mijadeira, urinando muito, olhos fundos, pele escura ao redor dos olhos, cavidade ocular profunda, desidratação, falta de água no corpo, sem beber água, diarreia, caganeira, excesso de evacuamento, falta de ar, dispneia, asfixia, sufocação, aperto no peito, ofegação, histórico familiar, escarro mucóide, mucosa sem parar, nariz e olhos lacrimejando, dor de cabeça, enxaqueca, cefaleia, tontura, vertigem, zonzo, perda de equilíbrio, dificuldade de se manter em pé, dificuldade em andar reto, desequilíbrio, falta de concentração, dificuldade de realizar uma tarefa por muito tempo, dificuldade de foco, rigidez no pescoço, torcicolo, dor no pescoço, depressão, tristeza extrema, desânimo, irritabilidade, ficar bravo com facilidade, impaciência, perturbações visuais, alucinações, distorção visual, dor nas costas, dor na lombar, dificuldade de se abaixar, dificuldade de levantar objetos pesados, fraqueza nos membros, cansaço, fadiga nos braços e pernas, dor no pescoço, dor ao virar a cabeça, dor para levantar os braços, fraqueza de um lado do corpo, falta de controle de um lado do corpo, fraqueza lateral, sensorium alterado, consumo de drogas, abstinência de drogas, urina escura, urina colorida com tom escuro, urina marrom, suor, suor excessivo, suando muito, dor muscular, dor nos músculos, dor na panturrilha, dor na coxa, dor no bíceps, febre leve, suor moderado, temperatura levemente elevada, linfonodos inchados, gânglios linfáticos inchados, inchaço nas glândulas, mal-estar, não estar bem, desconforto geral, manchas vermelhas no corpo, partes da pele com uma cor viva mais forte do que o normal, erupções vermelhas, dor nas articulações, dor nas juntas, desconforto nas articulações, dor atrás dos olhos, dor no fundo dos olhos, dor pulsante na parte interna dos olhos, constipação, defecando pouco, não defecando, aparência tóxica (tifoide), má aparência, zumbi, dor abdominal (barriga), vontade de ir ao banheiro sem vontade, desconforto estomacal, urina amarela, urina com cor forte mas sem sangue, urina com cor forte mas sem dor, recebimento de transfusão de sangue, recebimento de injeções não esterilizadas, coma, estado vegetativo, inconsciência, hemorragia estomacal, dores no estômago, sensação de enchimento estomacal, leve sentimento de fraqueza, dores após alimentação, falência hepática aguda, colapso hepático, falha hepática aguda, inchaço do estômago, estufamento, dilatação abdominal, distensão abdominal, inchaço abdominal, barriga inchada, histórico de consumo de álcool, bebida excessiva, alcoolismo, sobrecarga de líquidos, água em demasia, retenção de líquidos, catarro, mucosa escura no nariz, espirro com mucosa espessa, sangue no escarro, mucosa escura e com sangue no nariz, espirro com mucosa e sangue, irritação na garganta, dor de garganta, coceira na garganta, vermelhidão nos olhos, olhos vermelhos, olhos irritados, pressão sinusal, congestão sinusal, dor facial, nariz escorrendo, coriza, congestionamento, muito catarro, nariz entupido, perda de olfato, não sente cheiro, ausência de olfato, batimento cardíaco acelerado, coração acelerado, ansiedade, escarro enferrujado, catarro laranja, escarro alaranjado, dor ao evacuar, dor ao defecar, dor na região anal, proctalgia, dor retal, ardor anal, queimação anal, fezes com sangue, sangue ao defecar, sangue nas fezes, irritação no ânus, coceira no ânus, desconforto moderado no ânus, cãibras, espasmos musculares, contraturas musculares, hematomas, manchas roxas na pele, manchas doloridas na pele, pernas inchadas, sensação desconfortável nas pernas, pernas pesadas, sensação de formigamento nas pernas, vasos sanguíneos inchados, veias saltadas, formigamento nos membros, perda moderada de sensibilidade nos membros, veias salientes na panturrilha, varizes, veias saltadas nas pernas, ganho de peso, engordamento, ganho de gordura, mãos e pés frios, perda de sensibilidade nas pontas dos pés e mãos, diferença de temperatura do corpo com os membros, mudanças de humor, instabilidade emocional, irritabilidade, rosto e olhos inchados, inchaço facial, tireoide aumentada, hipertireoidismo, bócio, unhas quebradiças, unhas fracas, unhas frágeis, extremidades inchadas, formigamento nas extremidades dos membros, inchaço nas mãos e pés, menstruação anormal, menstruação irregular, menorragia, sangramento intermenstrual, metrorragia, fraqueza muscular, fadiga muscular, astenia, impotência muscular, ansiedade, apreensão, preocupação, pânico, medo, nervosismo, fala arrastada, fala enrolada, fala lenta, dicção prejudicada, palpitações, batimento forte do coração, lábios ressecados e formigantes, lábios quebradiços, lábios rachados, dor no joelho, incômodo no joelho, desconforto no joelho, dor na articulação do quadril, dor ao sentar, dor ao levantar, inchaço nas articulações, artrite, articulações inflamadas, dor ao caminhar, dor ao andar, desconforto ao caminhar, rigidez de movimento, bradicinesia, rigidez muscular, tontura (sensação de girar), atordoado, vertigem, instabilidade, ausência de estabilidade, pústulas cheias de pus, cravos, espinha, acne, crosta, crostas espessas, desconforto na bexiga, vontade de urinar, pressão na bexiga, cheiro forte da urina, odor intenso na urina, sensação contínua de urinar, descamação da pele, pele descascando, pele esfoliando, descamação prateada, psoríase, escamas prateadas, pequenos buracos nas unhas, pontuações nas unhas, unhas inflamadas, unhas avermelhadas, bolha, vesículas, erupção, ferida vermelha ao redor do nariz, dermatite perioral, inflamação perinasal, crosta amarela escorrendo, exsudato, secreção da ferida.
            **Exemplo de mensagem rotineira 1:** "Estou com dor de cabeça, dor de barriga, espirrando com a cabeça coçando e com manchas vermelhas.".
            **Resposta esperada 1:** "dor de cabeça, Dor de estômago, coceira, espirros contínuos, Manchas vermelhas no corpo".
            **Exemplo de mensagem rotineira 2:** "Ando com uma sensação de cansaço e um mal-estar que não consigo sacudir. Às vezes o estômago também não ajuda muito.".
            **Resposta esperada 2:** "Dor de estômago,Fadiga,Fraqueza nos membros,Mal-estar.".
            **Exemplo de mensagem rotineira 3:** "Minha unhas estão fracas e não estou sentido cheiro de nada.".
            **Resposta esperada 3:** "Unhas fracas, Não sente cheiro.".
            **Exemplo de mensagem rotineira 4:** "Sinto cansaço, me sinto desfocado e distante, ando me sentindo ansioso e deprimido.".
            **Resposta esperada 4:** "Fadiga, Falta de concentração, Depressão, Ansiedade.".
            Retorne apenas a lista de sintomas e nada mais, caso não encontre nenhum sintoma, retorne "Nenhum".
            Mensagem:
            {}'''.format(message),
        },
    ])
    print(result["message"]["content"])

    sintomas = buscar_referencias(result["message"]["content"], df)

    if len(sintomas) == 0:
        return {"sintomas": ["Nenhum"]}
    
    modelo = model(prediction_number=2)

    return {"sintomas": sintomas,
            "especialidade": modelo.predict(sintomas)}

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'
    )

df = pd.read_csv('assets/datasets/sintomas_variacoes.csv')

def buscar_referencias(texto, df):
    referencias_encontradas = []
    texto_normalizado = remover_acentos(texto.lower())
    lista = re.split(r'[,\n;]+|\s{2,}', texto_normalizado)
    lista = [item.strip() for item in lista if item.strip()]

    lista_recuperada = [recuperacao.recuperar_sentence(item) for item in lista]
    lista_recuperada = [remover_acentos(item.lower()) for item in lista_recuperada]
    for _, row in df.iterrows():
        referencia = row['referencia']
        referencia_normalizada = remover_acentos(referencia.lower())
        variacoes = row.drop('referencia').dropna().str.lower().apply(remover_acentos).tolist() 

        todas_variacoes = [referencia_normalizada] + variacoes

        regex = '|'.join(map(re.escape, todas_variacoes))

        for item in lista_recuperada:
            print(item)
            if re.search(regex, item):
                referencias_encontradas.append(referencia)
                lista_recuperada.remove(item)
                break
    print(referencias_encontradas)
    return referencias_encontradas

