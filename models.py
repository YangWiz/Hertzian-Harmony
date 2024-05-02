from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Questions(Base):
    __tablename__ = "Questions"

    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    uuid = Column(String, nullable=False)
    url = Column(String, nullable=False)
    voteYesPhone = Column(String, nullable=False)
    voteNoPhone = Column(String, nullable=False)
    yes = Column(Integer, nullable=False)
    no = Column(Integer, nullable=False)


class PhonePool(Base):
    __tablename__ = "PhonePool"

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False, unique=True)
    question_uuid = Column(String, nullable=True)
    question_type = Column(bool, nullable=True)
