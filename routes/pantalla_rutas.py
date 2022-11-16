from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.pantalla_esquema import pantallas
from models.pantalla_modelo import Pantalla
from starlette.status import HTTP_204_NO_CONTENT

pantalla = APIRouter()

@pantalla.post('/pantalla', response_model=Pantalla, tags=['Pantalla'])
def add_pantalla(pantalla: Pantalla):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.insert().values(pantalla.dict()))
    conexion.close()
    if resultado:
        return pantalla.dict()

@pantalla.get('/pantalla/{id_registro}', response_model=Pantalla, tags=['Pantalla'])
def get_pantalla(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.select().where(pantallas.c.idRegistro == id_registro)).first()
    conexion.close()
    if resultado:
        return resultado

@pantalla.delete('/pantalla/{id_registro}', status_code=HTTP_204_NO_CONTENT, tags=['Pantalla'])
def delete_pantalla(id_registro: str):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.delete().where(pantallas.c.idRegistro == id_registro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='pantalla no encontrada')

@pantalla.put('/pantalla/{id_registro}', response_model=Pantalla, tags=['Pantalla'])
def update_pantalla(pantalla_id: str, pantalla_actualizada: Pantalla):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.update().values(
        idRegistro = pantalla_id,
        modelo = pantalla_actualizada.modelo,
        resolucion = pantalla_actualizada.resolucion,
        calidad = pantalla_actualizada.calidad,
        tipoPantalla = pantalla_actualizada.tipoPantalla,
        tamanio = pantalla_actualizada.tamanio,
        frecuenciaRefresco = pantalla_actualizada.frecuenciaRefresco
    ).where(pantallas.c.idRegistro == pantalla_id))
    conexion.close()
    if resultado:
        pantalla_actualizada.idRegistro = pantalla_id
        return pantalla_actualizada.dict()

    raise HTTPException(status_code=404, detail='pantalla no encontrada')