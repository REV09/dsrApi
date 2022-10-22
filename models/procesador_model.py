from pydantic import BaseModel

class Procesador(BaseModel):
    idRegistro: str
    modelo: str
    marca: str
    numeroNucleos: int
    numeroHilos: int
    velocidadMaxima: float
    velocidadMinima: float
    litografia: int