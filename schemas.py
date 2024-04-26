from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    complete: bool

class UpdateItem(BaseModel):
    id: int
    name: str
    description: str
    complete: bool