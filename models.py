from sqlalchemy import String, Integer, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Questions(Base):
    __tablename__ = "Questions"

    id = Column(Integer, primary_key=True)
    prompt = Column(String, nullable=False)
    url = Column(String, nullable=False)
    voteYesPhone = Column(String, nullable=False)
    voteNoPhone = Column(String, nullable=False)
    yes = Column(Integer, primary_key=True)
    no = Column(Integer, primary_key=True)


class PhonePool(Base):
    __tablename__ = "PhonePool"

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
