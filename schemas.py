from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class CarCreate(BaseModel):
    model: str
    brand: str
    color: Optional[str] = None
    speed: Optional[str] = None
    year: int
    price: Decimal


class CarResponse(CarCreate):
    id: int

    class Config:
        orm_mode = True


class CarResponseMessage(BaseModel):
    msg: str
    car: CarResponse
