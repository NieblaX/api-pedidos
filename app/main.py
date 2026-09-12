from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers import usuarios, productos
from app.routers import usuarios, productos, pedidos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Pedidos",
    description="API REST para gestionar usuarios, productos y pedidos",
    version="1.0.0"
)
app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(pedidos.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de Pedidos funcionando correctamente"
    }