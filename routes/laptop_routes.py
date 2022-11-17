from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.laptops_esquema import laptops
from models.laptop_model import Laptop
from uuid import uuid4 as uuid
from starlette.status import HTTP_204_NO_CONTENT

laptop = APIRouter()

@laptop.get('/laptops', response_model=list[Laptop], tags=["laptops"])
def get_laptops():
    conexion = conexionDB()
    resultSet = conexion.execute(laptops.select()).fetchall()
    conexion.close()
    return resultSet


@laptop.post('/laptop', response_model=Laptop, tags=["laptops"])
def add_laptop(laptop: Laptop):
    laptop.idRegistro = str(uuid())
    conexion = conexionDB()
    result = conexion.execute(laptops.insert().values(laptop.dict()))
    lap = conexion.execute(laptops.select().where(laptops.c.idRegistro == laptop.idRegistro)).first()
    conexion.close()
    return lap


@laptop.get('/laptop/{laptop_id}', response_model=Laptop, tags=["laptops"])
def get_laptop(laptop_id: str):
    conexion = conexionDB()
    result = conexion.execute(laptops.select().where(laptops.c.idRegistro == laptop_id)).first()
    conexion.close()
    if result:
        return result

    raise HTTPException(status_code=404, detail="Laptop not found")

@laptop.delete('/laptop/{laptop_id}', status_code=HTTP_204_NO_CONTENT, tags=["laptops"])
def delete_laptop(laptop_id: str):
    conexion = conexionDB()
    result = conexion.execute(laptops.delete().where(laptops.c.idRegistro == laptop_id))
    conexion.close()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Laptop not found")

@laptop.put('/laptop/{laptop_id}', response_model=Laptop, tags=["laptops"])
def update_laptop(laptop_id: str, laptop_actualizada: Laptop):
    conexion = conexionDB()
    result = conexion.execute(laptops.update().values(idRegistro = laptop_id,
    modelo = laptop_actualizada.modelo,
    memoriaRam = laptop_actualizada.memoriaRam,
    tarjetaVideo = laptop_actualizada.tarjetaVideo,
    pantalla = laptop_actualizada.pantalla,
    almacenamiento = laptop_actualizada.almacenamiento,
    procesador = laptop_actualizada.procesador).where(laptops.c.idRegistro == laptop_id))
    conexion.close()
    if result:
        laptop_actualizada.idRegistro = laptop_id
        return laptop_actualizada.dict()

    raise HTTPException(status_code=404, detail="Laptop not found")