from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Vrijeme(Base):
    __tablename__ = 'Vrijeme'
    Datum = Column(String, primary_key=True)
    
    Temperatura = Column(Float)
    OsjecajTemperatura = Column(Float)
    MaksimalnaDnevna = Column(Float)
    MinimalnaDnevna = Column(Float)
    BrzinaVjetra = Column(Float)
    Vlaznost = Column(Float)
    DanUTjednu = Column(String)
   
    #Icon = Column(String(255))
    #Ikona = Column(String(255))
    #Uvjeti = Column(String(255))
    
    
    #Vjetar = Column(String(255))
    VrijemeDohvacanja = Column(String(255))
    VrijemeSljedecegDohvacanja = Column(String(255))
    Timestamp=Column(Integer)
    TimestampSljedecegDohvacanja=Column(Integer)
    Tlak = Column(Float)
    Grad=Column(String)
    Ikona=Column(String)
                        

'''
def __init__(self, temperatura, uvijeti, brzina_vjetra, vlaznost):
    self.temperatura = temperatura
    self.uvijeti = uvijeti
    self.brzina_vjetra = brzina_vjetra
    self.vlaznost = vlaznost
'''
