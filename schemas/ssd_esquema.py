from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import motor

meta = MetaData()

ssds = Table('ssd', meta,
    Column('idRegistro', String(50), primary_key=True),
    Column('marca', String(20)),
    Column('modelo', String(45)),
    Column('capacidad', Integer),
    Column('factorForma', String(20)),
    Column('durabilidad', String(20)),
    Column('tipoMemorias', String(5)),
    Column('generacionMemorias', String(10)),
    Column('velocidadLectura', String(20)),
    Column('velocidadEscritura', String(20)),
    Column('protocolo', String(10)))

engine = motor()
meta.create_all(engine)
