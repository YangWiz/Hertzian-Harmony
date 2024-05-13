from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    complete: bool

class Phone(BaseModel):
    number: str

class Question(BaseModel):
    uuid: str
    description: str
