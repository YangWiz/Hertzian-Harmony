from typing import Union
from fastapi import FastAPI
import inflect
from fastapi import FastAPI, Depends
from schemas import Item, Phone, Question
from sqlalchemy.orm import Session
from database import db
from models import Base
import models
import os
import uuid
from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from vxml_builder import QuestionBuilder, HomeBuilder
import urllib.parse

app = FastAPI()

ENV_VAR_DB_URL = "DATABASE_URL"
HEROKU_URL = "HEROKU_URL"

db_url = os.getenv(ENV_VAR_DB_URL, "localhost")
heroku_url = os.getenv(HEROKU_URL, "localhost")
db_url = db_url.replace('postgres', 'postgresql')

psql = db(db_url)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/api/new_phone/{phone}")
def add_new_phone(phone: str, db: Session = Depends(psql.connect)):
    new_phone = models.PhonePool(phone = phone)
    db.add(new_phone)

    db.commit()
    db.refresh(new_phone)
    return new_phone

@app.get("/api/all_phones")
def all_phones(db: Session = Depends(psql.connect)):
    return db.query(models.PhonePool).all()

@app.get("/api/free_phones")
def free_phones(db: Session = Depends(psql.connect)):
    return db.query(models.PhonePool).filter(models.PhonePool.answer_type == None).all()

@app.get("/api/vote/{number}")
def vote(number: str, db: Session = Depends(psql.connect)):
    new_phone = models.PhonePool(number = number)
    db.add(new_phone)
    return

@app.get("/api/questions")
def all_questions(db: Session = Depends(psql.connect)):
    return db.query(models.Questions).all()

@app.post("/api/questions")
def add_question(question: Question, db: Session = Depends(psql.connect)):
    phones = get_free_phones(db)
    if (len(phones) < 2):
        return "No enough free phones (needs >= 2)."

    quuid = uuid.uuid4()
    yes, no = phones
    question = models.Questions(
        prompt = question.description,
        uuid = str(quuid),
        url = heroku_url + "/vxml/" + str(quuid) + ".xml",
        voteYesPhone = yes,
        voteNoPhone = no,
        yes = 0,
        no = 0,
    )

    qbuilder = QuestionBuilder(0, 0, heroku_url, str(quuid))
    qbuilder.commit()

    vxml = HomeBuilder()
    # updated_vxml = vxml.delete_menu_option(9)
    options = {}
    options["prompt"] = question.prompt
    options["url"] = question.url
    vxml.updated_vxml([options])
    vxml.commit()

    # Get free phone from the phone pool.
    db.add(question)
    db.commit()
    db.refresh(question)
    return question 

def get_free_phones(db: Session = Depends(psql.connect)):
    phones = db.query(models.PhonePool).filter(models.PhonePool.answer_type == None).all()
    if (len(phones) <= 1):
        return [] 
    else:
        phones[0].phone


        db.add(curr_item)
        db.commit()
        db.refresh(curr_item)
        return [phones[0].phone, phones[1].phone]

@app.get("/vxml/{path}", response_class=FileResponse)
def fetch_files(path: str):
    # Decode URL-encoded characters
    decoded_string = urllib.parse.unquote(path)
    return "vxml/" + decoded_string
