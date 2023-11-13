from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Admin(Base):
    __tablename__ = "Admin"
    korisnickoIme = Column(String, primary_key=True)
    lozinka = Column(String)
