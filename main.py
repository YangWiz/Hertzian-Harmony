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

ENV_VAR_DB_HOST = "DB_HOST"
ENV_VAR_DB_PORT = "DB_PORT"
ENV_VAR_DB_NAME = "POSTGRES_DB"
ENV_VAR_DB_USERNAME = "POSTGRES_USER"
ENV_VAR_DB_PASSWORD = "POSTGRES_PASSWORD"

db_host = os.getenv(ENV_VAR_DB_HOST, "localhost")
db_port = os.getenv(ENV_VAR_DB_PORT, "5432")
db_name = os.getenv(ENV_VAR_DB_NAME, "postgres")
db_username = os.getenv(ENV_VAR_DB_USERNAME, "postgres")
db_password = os.getenv(ENV_VAR_DB_PASSWORD, "test")

db_url = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
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

