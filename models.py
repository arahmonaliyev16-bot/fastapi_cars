from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime
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


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)