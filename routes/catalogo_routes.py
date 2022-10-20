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

@catalogo.get('/catalogo/{idRegistro}', response_model=Catalogo,tags=["Catalogo"])
def get_catalogo(idRegistro: str):
    conexion = conexionDB()
    result = conexion.execute(catalogos.select().where(catalogos.c.idRegistro == idRegistro)).first()
    conexion.close()
    if result:
        return result

@catalogo.post('/catalogo', response_model=Catalogo,tags=["Catalogo"])
def addRegistro(registro: Catalogo):
    conexion = conexionDB()
    result = conexion.execute(catalogos.insert().values(registro.dict()))
    conexion.close()
    if result:
        return registro.dict()

@catalogo.delete('/catalogo/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=["Catalogo"])
def delete_catalogo(idRegistro: str):
    conexion = conexionDB()
    result = conexion.execute(catalogos.delete().where(catalogos.c.idRegistro == idRegistro))
    conexion.close()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="catalogo not found")