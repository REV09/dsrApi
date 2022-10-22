from pydantic import BaseModel

class TarjetaVideo(BaseModel):
    idRegistro: str
    modelo: str
    marca: str
    cantidadVram: int
    tipoMemoria: str
    bits: int
    velocidadReloj: float
    tipo: str