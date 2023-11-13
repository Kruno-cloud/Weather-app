from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from Models.Vrijeme import Vrijeme

Base = declarative_base()

class Grad(Base):
    __tablename__ = 'Gradovi'
    id = Column(Integer, primary_key=True)
    grad = Column(String)
    vrijemeId=Column(Integer, ForeignKey('vrijeme.ID'))

'''
def __init__(self, temperatura, uvijeti, brzina_vjetra, vlaznost):
    self.temperatura = temperatura
    self.uvijeti = uvijeti
    self.brzina_vjetra = brzina_vjetra
    self.vlaznost = vlaznost
'''
