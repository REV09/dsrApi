from fastapi import APIRouter, HTTPException, Response
from config.db import conexionDB
from schemas.memoria_ram_esquema import memoria_rams
from models.memoria_ram_modelo import MemoriaRam
from starlette.status import HTTP_204_NO_CONTENT

memoria_ram = APIRouter()


@memoria_ram.post("/memoria", response_model=MemoriaRam, tags=["Memoria Ram"])
def add_memoriaRam(memoria: MemoriaRam):
    conexion = conexionDB()
    result = conexion.execute(memoria_rams.insert().values(memoria.dict()))
    conexion.close()
    if result:
        return memoria.dict()


@memoria_ram.get('/memoria/{id_registro}', response_model=MemoriaRam,
                 tags=['Memoria Ram'])
def get_memoriaRam(id_registro: str):
    conexion = conexionDB()
    result = conexion.execute(memoria_rams.select().where(
        memoria_rams.c.idRegistro == id_registro)).first()
    conexion.close()
    if result:
        return result


@memoria_ram.delete('/memoria/{id_registro}', status_code=HTTP_204_NO_CONTENT,
                    tags=['Memoria Ram'])
def delete_memoria(id_registro: str):
    conexion = conexionDB()
    result = conexion.execute(memoria_rams.delete().where(
        memoria_rams.c.idRegistro == id_registro))
    conexion.close()
    if result:
        return Response(status_code=HTTP_204_NO_CONTENT)


@memoria_ram.put('/memoria/{id_registro}', response_model=MemoriaRam,
                 tags=['Memoria Ram'])
def update_memoriaRam(ram_id: str, memoria_ram_actualizada: MemoriaRam):
    conexion = conexionDB()
    result = conexion.execute(memoria_rams.update().values(
        idRegistro=ram_id,
        modelo=memoria_ram_actualizada.modelo,
        marca=memoria_ram_actualizada.marca,
        tipoMemoria=memoria_ram_actualizada.tipoMemoria,
        cantidadMemoria=memoria_ram_actualizada.cantidadMemoria,
        cantidadMemorias=memoria_ram_actualizada.cantidadMemorias,
        velocidad=memoria_ram_actualizada.velocidad,
        ecc=memoria_ram_actualizada.ecc).where(
        memoria_rams.c.idRegistro == ram_id))
    conexion.close()
    if result:
        memoria_ram_actualizada.idRegistro = ram_id
        return memoria_ram_actualizada.dict()

    raise HTTPException(status_code=404, detail="Memoria Ram not found")
