from typing import Optional, TYPE_CHECKING, List
from sqlmodel import SQLModel, Field, Relationship
from decimal import Decimal
from sqlalchemy import Column, Integer, ForeignKey, Boolean, Numeric, Text
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.base import Base

if TYPE_CHECKING:
    from app.modules.categorias.models import Categoria
    from app.modules.ingredientes.models import Ingrediente


class ProductoIngrediente(SQLModel, table = True):

    __tablename__ = "Producto_Ingrediente"

    producto_id: int = Field(
        sa_column = Column(Integer, ForeignKey("Producto.id", ondelete = "CASCADE"), primary_key = True)
    )

    ingrediente_id: int = Field(
        sa_column = Column(Integer, ForeignKey("Ingrediente.id", ondelete = "CASCADE"), primary_key = True)
    )

    es_removible: bool = Field(nullable = False, default = False)


class ProductoCategoria(SQLModel, table = True):

    __tablename__ = "Producto_Categoria"

    producto_id: int = Field(
        sa_column = Column(Integer, ForeignKey("Producto.id", ondelete = "CASCADE"), primary_key = True)
    )

    categoria_id: int = Field(
        sa_column = Column(Integer, ForeignKey("Categoria.id", ondelete = "CASCADE"), primary_key = True)
    )

    es_principal: bool = Field(
        sa_column = Column(Boolean, default = False, nullable = False)
    )
    

class Producto(Base, table = True):

    __tablename__ = "Producto"

    nombre: str = Field(min_length = 2, max_length = 150, nullable = False)

    descripcion: Optional[str] = Field(default = None)

    precio_base: Decimal = Field(
        sa_column = Column(Numeric(10,2), nullable = False)
    )

    imagenes_url: List[str] = Field(default_factory = list, sa_column = Column(ARRAY(Text), nullable = False))

    stock_cantidad: int = Field(default = 0, ge = 0, nullable = False)

    disponible: Optional[bool] = Field(default = True, nullable = False)

    categorias: List["Categoria"] = Relationship(back_populates = "productos", link_model = ProductoCategoria)

    ingredientes: List["Ingrediente"] = Relationship(back_populates = "productos", link_model = ProductoIngrediente)
