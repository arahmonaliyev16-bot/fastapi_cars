from sqlalchemy import Column, Integer, String, Text, Numeric
from database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(200), nullable=False)
    brand = Column(String(200), nullable=False)
    color = Column(String(200), nullable=False)
    speed = Column(String(200), nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Numeric(10,2))


