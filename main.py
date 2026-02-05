from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import engine, get_db
from models import Car


app = FastAPI(title="FastAPI Cars")

models.Base.metadata.create_all(bind=engine)

@app.post("/cars", response_model=schemas.CarResponseMessage)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    car = crud.create_car(db, car)
    data = {
        'msg': 'Car created',
        'car': car
    }
    return data

@app.get("/cars", response_model=list[schemas.CarResponse])
def view_cars(db: Session = Depends(get_db)):
    return crud.get_cars(db)


@app.get("/cars/{car_id}", response_model=schemas.CarResponse)
def view_car(car_id: int, db: Session = Depends(get_db)):
    car = crud.get_car(db, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@app.patch("/cars/{car_id}", response_model=schemas.CarResponse)
def update_car(car_id: int, car: schemas.CarCreate, db: Session = Depends(get_db)):
    updated = crud.update_car(db, car_id, car)
    if not updated:
        raise HTTPException(status_code=404, detail="Car not found")
    return updated


@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_car(db, car_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted"}
