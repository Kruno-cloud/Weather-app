from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Kontakt(Base):
    __tablename__ = 'kontakt_podaci'
    id = Column(Integer, primary_key=True)
    adresa = Column(String)
    telefon = Column(Integer)
    email = Column(String)
