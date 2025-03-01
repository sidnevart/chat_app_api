from pydantic import BaseModel

class GroupCreate(BaseModel):
    name: str
    creator_id: int

class GroupResponse(BaseModel):
    id: int
    name: str
    creator_id: int

    class Config:
        orm_mode = True