from pydantic import BaseModel, ConfigDict
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
    model_config = ConfigDict(from_attributes = True)


class CarResponseMessage(BaseModel):
    msg: str
    car: CarResponse


class CarUpdate(BaseModel):
    model: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[Decimal] = None
    color: Optional[str] = None
    year: Optional[int] = None
    speed: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserSignup(BaseModel):
    username: str
    email: str
    password: str


class Settings(BaseModel):
    auth_jwt_secret_key: str = 'e11d8220daab475f36f2c9ee514bb36ec3e4f4c57ff2497b6768bd5f16d84a27'


class LoginModel(BaseModel):
    email_username: str
    password: str


class ProfileUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
