from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Сущность
class Car(BaseModel):
    id: int
    make: str
    model: str
    year: int

# Хранилище
cars = []

# Инициализация 
def initialize_cars():
    sample_cars = [
        Car(id=1, make="Toyota", model="Camry", year=2020),
        Car(id=2, make="Honda", model="Civic", year=2019),
        Car(id=3, make="Ford", model="Mustang", year=2021),
    ]
    return sample_cars

cars = initialize_cars()

# Получить список всех машин
@app.get("/cars", response_model=List[Car])
def get_cars():
    return cars

# Добавить новую машину
@app.post("/cars", response_model=Car)
def add_car(car: Car):
    if any(c.id == car.id for c in cars):
        raise HTTPException(status_code=400, detail="Car with this ID already exists.")
    cars.append(car)
    return car

# Получить машину по ID
@app.get("/cars/{car_id}", response_model=Car)
def get_car(car_id: int):
    car = next((car for car in cars if car.id == car_id), None)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car

# Удалить машину по ID
@app.delete("/cars/{car_id}", response_model=dict)
def delete_car(car_id: int):
    global cars
    cars = [car for car in cars if car.id != car_id]
    return {"message": "Car deleted"}

# Запуск приложения (вместо этого вы можете использовать uvicorn из командной строки)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
