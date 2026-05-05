from typing import Optional, List
from sqlmodel import SQLModel, Field
from decimal import Decimal

class CategoriaInput(SQLModel):

    categoria_id: int

    es_principal: bool = False

class IngredienteInput(SQLModel):

    ingrediente_id: int
    
    es_removible: bool = False

class ProductoCreate(SQLModel):

    nombre: str = Field(min_length=2, max_length=150)

    descripcion: Optional[str] = None

    precio_base: Decimal = Field(ge=0)

    imagenes_url: List[str] = Field(default_factory=list)

    stock_cantidad: int = Field(default=0, ge=0)

    disponible: Optional[bool] = Field(default=True)

    categorias: List[CategoriaInput] = Field(default_factory=list)

    ingredientes: List[IngredienteInput] = Field(default_factory=list)

class ProductoUpdate (SQLModel):

    nombre: Optional[str] = Field(default = None, min_length = 2, max_length = 150)

    descripcion: Optional[str] = Field(default = None, min_length = 2, max_length = 100)

    precio_base: Optional[Decimal] = Field(default = None, ge = 0)

    imagenes_url: Optional[List[str]] = Field(default = None)

    stock_cantidad: Optional[int] = Field(default = None, ge = 0)

    disponible: Optional[bool] = None

class ProductoPublic(SQLModel):
    id: int

    nombre: str

    descripcion: Optional[str]

    precio_base: Decimal

    imagenes_url: List[str]

    stock_cantidad: int

class ProductoList(SQLModel):

    data: List[ProductoPublic]

    total: int
    

