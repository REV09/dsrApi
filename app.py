from fastapi import FastAPI
from routes.laptop_routes import laptop
from routes.memoriaRam_routes import memoriaRam
from routes.catalogo_routes import catalogo
from routes.procesador_rutas import procesador
from routes.tarjeta_de_video_rutas import tarjetaVideo
from routes.pantalla_rutas import pantalla
from routes.almacenamiento_rutas import almacenamiento
from routes.hdd_rutas import hdd
from routes.ssd_rutas import ssd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Laptop API DSR',
    description='Api de obtencion de informacion de hardware de laptops',
    openapi_tags=[{
        'name' : 'laptops',
        'description' : 'laptops routes CRUD'
    },
    {
        'name' : 'Memoria Ram',
        'description' : 'Memorias Ram routes CRUD'
    },
    {
        'name' : 'Catalogo',
        'description' : 'Catalogo routes CRUD'
    },
    {
        'name' : 'Procesador',
        'description' : 'Procesador routes CRUD'
    },
    {
        'name' : 'Tarjeta de video',
        'description' : 'Tarjeta de video routes CRUD'
    },
    {
        'name' : 'Pantalla',
        'description' : 'Pantalla routes CRUD'
    },
    {
        'name' : 'Almacenamiento',
        'description' : 'Almacenamiento routes CRUD'
    },
    {
        'name' : 'HDD',
        'description' : 'HDD routes CRUD'
    },
    {
        'name' : 'SSD',
        'description' : 'SSD routes CRUD'
    }
    ]
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(laptop)
app.include_router(memoriaRam)
app.include_router(catalogo)
app.include_router(procesador)
app.include_router(tarjetaVideo)
app.include_router(pantalla)
app.include_router(almacenamiento)
app.include_router(hdd)
app.include_router(ssd)