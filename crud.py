from sqlalchemy import or_
from sqlalchemy.orm import Session
from models import Car
from schemas import CarCreate


def create_car(db: Session, car: CarCreate):
    new_car = Car(**car.dict())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car


def get_cars(db: Session):
    return db.query(Car).all()


def get_car(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()


def update_car(db: Session, car_id: int, car: CarCreate,):
    db_car = get_car(db, car_id)
    if not db_car:
        return None

    for key, value in car.dict().items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: int):
    car = get_car(db, car_id)
    if not car:
        return None

    db.delete(car)
    db.commit()
    return car


def search_cars(
        db: Session,
        q: str,
):
    return(
        db.query(Car).filter(or_(Car.model.ilike(f"%{q}%"), Car.brand.ilike(f"%{q}%"))).all()
    )


def get_cars_pagination(db: Session, skip: int = 0, limit: int = 10):
    return(
        db.query(Car).offset(skip).limit(limit).all()
    )


def partial_update_car(db: Session, car_id: int, car_data: dict):
    db_car = get_car(db, car_id)
    if not db_car:
        return None

    for key, value in car_data.items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)
    return db_car