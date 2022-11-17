from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, Integer, DECIMAL
from config.db import motor

meta = MetaData()

procesadores = Table('procesador', meta,
    Column('idRegistro', String(50), primary_key=True),
    Column('modelo', String(45)),
    Column('marca', String(45)),
    Column('numeroNucleos', Integer),
    Column('numeroHilos', Integer),
    Column('velocidadMaxima', DECIMAL),
    Column('velocidadMinima', DECIMAL),
    Column('litografia', Integer))

engine = motor()
meta.create_all(engine)
