from pydantic import BaseModel

class MessageRequest(BaseModel):
    def __init__(self, message: str):
        self.message = message