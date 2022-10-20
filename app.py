from fastapi import FastAPI
from routes.laptop_routes import laptop
from routes.memoriaRam_routes import memoriaRam
from routes.catalogo_routes import catalogo

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
    }]
)

app.include_router(laptop)
app.include_router(memoriaRam)
app.include_router(catalogo)