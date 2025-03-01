from pydantic import BaseModel

class ChatCreate(BaseModel):
    name: str
    type: str

class ChatResponse(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        orm_mode = True