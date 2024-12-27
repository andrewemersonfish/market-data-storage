from sqlalchemy import Column, BigInteger, Integer, Float, Text
from ..base import Base

class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(BigInteger, primary_key=True)
    ticker = Column(Text)
    conditions = Column(Float)
    correction = Column(Integer)
    exchange = Column(Integer)
    price = Column(Float)
    sip_timestamp = Column(BigInteger)
    size = Column(Integer)