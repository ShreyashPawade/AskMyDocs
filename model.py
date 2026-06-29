from pydantic import BaseModel

class ChatRequest(BaseModel):
    
    session_id:str

    question: str

class Source(BaseModel):
    source:str
    page:int

    
class ChatResponse(BaseModel):
    context:str
    sources:list[Source]
    confidence:float    