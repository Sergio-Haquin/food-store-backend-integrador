from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from app.modules.health.router import router as health_router
from app.modules.productos.router import router as productos_router
from app.modules.categorias.router import router as categorias_router
from app.modules.ingredientes.router import router as ingredientes_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title = "Food Store API",
    description = "API para la gestión de productos en una tienda de alimentos",
    version = "1.0.0",
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(productos_router, prefix = "/productos", tags = ["Productos"])
app.include_router(categorias_router, prefix = "/categorias", tags = ["Categorias"])
app.include_router(ingredientes_router, prefix = "/ingredientes", tags = ["Ingredientes"]) 
