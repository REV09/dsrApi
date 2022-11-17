from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, Integer
from config.db import motor

meta = MetaData()

pantallas = Table('pantalla', meta,
                  Column('idRegistro', String(45), primary_key=True),
                  Column('modelo', String(45)),
                  Column('resolucion', String(20)),
                  Column('calidad', String(5)),
                  Column('tipoPantalla', String(10)),
                  Column('tamanio', String(10)),
                  Column('frecuenciaRefresco', Integer))

engine = motor()
meta.create_all(engine)
