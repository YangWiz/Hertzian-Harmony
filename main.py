from typing import Union
from fastapi import FastAPI
import inflect
from fastapi import FastAPI, Depends
from schemas import Item, UpdateItem
from sqlalchemy.orm import Session
from database import db
from models import Base
import logging
import models
import os

app = FastAPI()

ENV_VAR_DB_URL = "DATABASE_URL"

db_url = os.getenv(ENV_VAR_DB_URL, "localhost")

psql = db(db_url)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/new_phone/{}")
def add_new_phone():
    return

@app.get("")
def get_questions():
    return

@app.post("/api/list")
def add_item(item: Item, db: Session = Depends(psql.connect)):
    new_item = models.Item(name = item.name, description = item.description, complete = False)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

