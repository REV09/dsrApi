from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.pantalla_esquema import pantallas
from models.pantalla_modelo import Pantalla
from starlette.status import HTTP_204_NO_CONTENT

pantalla = APIRouter()

#Test
@pantalla.post('/pantalla', response_model=Pantalla, tags=['Pantalla'])
def add_pantalla(pantalla: Pantalla):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.insert().values(pantalla.dict()))
    conexion.close()
    if resultado:
        return pantalla.dict()

#Test
@pantalla.get('/pantalla/{idRegistro}', response_model=Pantalla, tags=['Pantalla'])
def get_pantalla(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.select().where(pantallas.c.idRegistro)).first()
    conexion.close()
    if resultado:
        return resultado

#Test
@pantalla.delete('/pantalla/{idRegistro}', status_code=HTTP_204_NO_CONTENT, tags=['Pantalla'])
def delete_pantalla(idRegistro: str):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.delete().where(pantallas.c.idRegistro == idRegistro))
    conexion.close()
    if resultado:
        return Response(status_code=HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail='pantalla no encontrada')

#Test
@pantalla.put('/pantalla/{idRegistro}', response_model=Pantalla, tags=['Pantallla'])
def update_pantalla(pantalla_id: str, pantallaActualizada: Pantalla):
    conexion = conexionDB()
    resultado = conexion.execute(pantallas.update().values(
        idRegistro = pantalla_id,
        modelo = pantallaActualizada.modelo,
        resolucion = pantallaActualizada.resolucion,
        calidad = pantallaActualizada.calidad,
        tipoPantalla = pantallaActualizada.tipoPantalla,
        tamanio = pantallaActualizada.tamanio,
        frecuenciaRefresco = pantallaActualizada.frecuenciaRefresco
    ).where(pantallas.c.idRegistro == pantalla_id))
    conexion.close()
    if resultado:
        pantallaActualizada.idRegistro = pantalla_id
        return pantallaActualizada.dict()

    raise HTTPException(status_code=404, detail='pantalla no encontrada')