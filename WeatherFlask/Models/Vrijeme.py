from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vrijeme(Base):
    __tablename__ = 'vremenski_podaci'
    id = Column(Integer, primary_key=True)
    temperatura = Column(Float)
    uvjeti = Column(String(255))
    brzina_vjetra = Column(Float)
    vlaznost = Column(Float)

   # def __init__(self, temperatura, uvijeti, brzina_vjetra, vlaznost):
   #     self.temperatura = temperatura
   #     self.uvijeti = uvijeti
   #     self.brzina_vjetra = brzina_vjetra
   #     self.vlaznost = vlaznost
