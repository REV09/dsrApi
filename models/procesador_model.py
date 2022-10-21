from argparse import OPTIONAL
from optparse import Option
from typing import Optional
from pydantic import BaseModel

class Procesador(BaseModel):
    idRegistro: str
    modelo: str
    marca: str
    numeroNucleos: int
    numeroHilos: int
    velocidadMaxima: float
    velocidadMinima: float
    litografia: str