from ast import main
from sqlalchemy import create_engine, MetaData

def conexionDB():
    engine = create_engine("mysql+pymysql://S19014007:HALOcea206-@dsr-server.mysql.database.azure.com:3306/laptops-dsr")
    conexion = engine.connect()
    return conexion

def motor():
    engine = create_engine("mysql+pymysql://S19014007:HALOcea206-@dsr-server.mysql.database.azure.com:3306/laptops-dsr")
    return engine