from typing import List
from fastapi import APIRouter, Response, HTTPException
from config.db import conexionDB
from schemas.catalogo_schema import catalogos
from models.catalogo_model import Catalogo
from starlette.status import HTTP_204_NO_CONTENT

catalogo = APIRouter()

@catalogo.get('/catalogos', response_model=List[Catalogo],tags=["Catalogo"])
def get_catalogos():
    conexion = conexionDB()
    resultSet = conexion.execute(catalogos.select()).fetchall()
    conexion.close()
    return resultSet

@catalogo.get('/catalogo/{id_registro}', response_model=Catalogo,tags=["Catalogo"])
def get_catalogo(id_registro: str):
    conexion = conexionDB()
    result = conexion.execute(catalogos.select().where(catalogos.c.idRegistro == id_registro)).first()
    conexion.close()
    if result:
        return result

@catalogo.post('/catalogo', response_model=Catalogo,tags=["Catalogo"])
def add_catalogo(registro: Catalogo):
    conexion = conexionDB()
    result = conexion.execute(catalogos.insert().values(registro.dict()))
    conexion.close()
    if result:
        return registro.dict()

@catalogo.delete('/catalogo/{id_registro}', status_code=HTTP_204_NO_CONTENT, tags=["Catalogo"])
def delete_catalogo(id_registro: str):
    conexion = conexionDB()
    result = conexion.execute(catalogos.delete().where(catalogos.c.idRegistro == id_registro))
    conexion.close()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="catalogo not found")

@catalogo.put('/catalogo/{id_registro}', response_model=Catalogo, tags=["Catalogo"])
def update_catalogo(catalogo_id: str, catalago_actualizado: Catalogo):
    conexion = conexionDB()
    result = conexion.execute(catalogos.update().values(
        idRegistro = catalogo_id,
        modelo = catalago_actualizado.modelo
    ).where(catalogos.c.idRegistro == catalogo_id))
    conexion.close()
    if result:
        catalago_actualizado.idRegistro = catalogo_id
        return catalago_actualizado.dict()

    raise HTTPException(status_code=404, detail="Catalogo not found")