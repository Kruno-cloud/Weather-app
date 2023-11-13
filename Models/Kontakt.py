from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Kontakt(Base):
    __tablename__ = 'Kontakt'
    Id = Column(Integer, primary_key=True)
    Adresa = Column(String)
    Telefon = Column(Integer)
    Email = Column(String)
