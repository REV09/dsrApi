from pydantic import BaseModel

class Hdd(BaseModel):
    idRegistro: str
    capacidad: str
    interfaz: str
    cache: str
    revoluciones: int
    tamanio: str