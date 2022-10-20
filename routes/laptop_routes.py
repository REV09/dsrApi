from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.laptops_schema import Laptops
from models.laptop_model import Laptop
from uuid import uuid4 as uuid
from starlette.status import HTTP_204_NO_CONTENT

laptop = APIRouter()

@laptop.get('/')
def read_root():
    return {'mensage': 'Welcome to REST API'}

@laptop.get('/laptops', response_model=list[Laptop], tags=["laptops"])
def get_laptops():
    conexion = conexionDB()
    resultSet = conexion.execute(Laptops.select()).fetchall()
    conexion.close()
    return resultSet


@laptop.post('/laptop', response_model=Laptop, tags=["laptops"])
def add_laptop(laptop: Laptop):
    laptop.idRegistro = str(uuid())
    conexion = conexionDB()
    result = conexion.execute(Laptops.insert().values(laptop.dict()))
    lap = conexion.execute(Laptops.select().where(Laptops.c.idRegistro == laptop.idRegistro)).first()
    conexion.close()
    return lap


@laptop.get('/laptop/{laptop_id}', response_model=Laptop, tags=["laptops"])
def get_laptop(laptop_id: str):
    conexion = conexionDB()
    result = conexion.execute(Laptops.select().where(Laptops.c.idRegistro == laptop_id)).first()
    conexion.close()
    if result:
        return result

    raise HTTPException(status_code=404, detail="Laptop not found")

@laptop.delete('/laptop/{laptop_id}', status_code=HTTP_204_NO_CONTENT, tags=["laptops"])
def delete_laptop(laptop_id: str):
    conexion = conexionDB()
    result = conexion.execute(Laptops.delete().where(Laptops.c.idRegistro == laptop_id))
    conexion.close()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Laptop not found")

@laptop.put('/laptop/{laptop_id}', response_model=Laptop, tags=["laptops"])
def update_laptop(laptop_id: str, laptopUpdate: Laptop):
    conexion = conexionDB()
    result = conexion.execute(Laptops.update().values(idRegistro = laptop_id,
    modelo = laptopUpdate.modelo,
    memoriaRam = laptopUpdate.memoriaRam,
    tarjetaVideo = laptopUpdate.tarjetaVideo,
    pantalla = laptopUpdate.pantalla,
    almacenamiento = laptopUpdate.almacenamiento,
    procesador = laptopUpdate.procesador).where(Laptops.c.idRegistro == laptop_id))
    conexion.close()
    if result:
        laptopUpdate.idRegistro = laptop_id
        return laptopUpdate.dict()

    raise HTTPException(status_code=404, detail="Laptop not found")