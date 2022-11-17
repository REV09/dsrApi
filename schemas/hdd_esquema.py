from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import motor

meta = MetaData()

hdds = Table('hdd', meta,
             Column('idRegistro', String(50), primary_key=True),
             Column('marca', String(20)),
             Column('modelo', String(45)),
             Column('capacidad', Integer),
             Column('interfaz', String(10)),
             Column('cache', Integer),
             Column('revoluciones', Integer),
             Column('tamanio', String(5)))

engine = motor()
meta.create_all(engine)
