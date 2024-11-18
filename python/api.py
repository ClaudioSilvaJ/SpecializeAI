from fastapi import FastAPI
from SymptomExtractor import SymptomExtractor
from MessageProcessor import MessageProcessor
from MessageRequest import MessageRequest

app = FastAPI()
extractor = SymptomExtractor('assets/datasets/sintomas_variacoes.csv')
processor = MessageProcessor(extractor)

@app.post("/extract-symptoms")
async def extract_symptoms(request: MessageRequest):
    response = await processor.process_message(request.message)
    return response
