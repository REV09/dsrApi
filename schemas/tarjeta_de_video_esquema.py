from sqlalchemy import Table, Column, MetaData
from sqlalchemy.sql.sqltypes import String, FLOAT
from config.db import motor

meta = MetaData()

tarjetasVideo = Table('tarjetavideo', meta,
                Column('idRegistro', String(50), primary_key=True),
                Column('modelo', String(45)),
                Column('marca', String(45)),
                Column('cantidadVram', int),
                Column('tipoMemoria', String(10)),
                Column('bits', int),
                Column('velocidadReloj', FLOAT),
                Column('tipo', String(10)),
                )

engine = motor()
meta.create_all(engine)