from sqlalchemy import Column, BigInteger, Integer, Float, Text
from ..base import Base

class MinuteAgg(Base):
    __tablename__ = "minute_aggs"
    
    id = Column(BigInteger, primary_key=True)
    ticker = Column(Text)
    volume = Column(Integer)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    window_start = Column(Integer)
    transactions = Column(Integer)