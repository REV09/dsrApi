from pydantic import BaseModel

class Hdd(BaseModel):
    idRegistro: str
    marca: str
    modelo: str
    capacidad: int
    interfaz: str
    cache: int
    revoluciones: int
    tamanio: str