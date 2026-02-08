from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pip._internal.network import auth
from sqlalchemy.orm import Session
import crud, models, schemas
from schemas import LoginModel, Settings
from database import engine, SessionLocal
from models import Car
from router_auth import auth_routers
from fastapi_jwt_auth import AuthJWT


app = FastAPI(title="FastAPI Cars")
app.include_router(auth_routers)


@AuthJWT.load_config
def get_config():
    return Settings()


models.Base.metadata.create_all(bind=engine)

# Database session olish uchun
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



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


@app.put("/cars/{car_id}", response_model=schemas.CarResponse)
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


@app.get("/cars-pagination", response_model=list[schemas.CarResponse])
def view_cars(
        page: int = 1,
        limit: int = 10,
        db: Session = Depends(get_db)):
        skip = (page - 1) * limit
        return crud.get_cars_pagination(db, skip=skip, limit=limit)


@app.get("/cars-search", response_model=list[schemas.CarResponse])
def search_cars(
        q: str,
        db: Session = Depends(get_db)):
        return crud.search_cars(db, q)


@app.patch("/cars/{car_id}", response_model=schemas.CarResponse)
def partial_update_car(
        car_id: int,
        car: schemas.CarCreate,
        db: Session = Depends(get_db)):
        updated = crud.partial_update_car(db, car_id, car.dict(exclude_unset=True))

        if not updated:
            raise HTTPException(status_code=404, detail="Car not found")
        return updated
