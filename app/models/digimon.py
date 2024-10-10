from app.config.database import Base
from sqlalchemy import Column, Integer,String, Float

class Digimon(Base):
    __tablename__ = 'digimon'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tipo = Column(String)
    hp = Column(Integer)
    ataque = Column(Float)