from sqlalchemy import Column, BigInteger, Integer, Float, Text
from ..base import Base

class DayAgg(Base):
    __tablename__ = "day_aggs"
    
    id = Column(BigInteger, primary_key=True)
    ticker = Column(Text)
    volume = Column(Integer)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    window_start = Column(Integer)
    transactions = Column(Integer)