from pydantic import BaseModel


class Pantalla(BaseModel):
    idRegistro: str
    modelo: str
    resolucion: str
    calidad: str
    tipoPantalla: str
    tamanio: str
    frecuenciaRefresco: int
