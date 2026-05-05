from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from sqlalchemy import Column, Integer, ForeignKey
from app.core.base import Base
from app.modules.productos.models import ProductoCategoria

if TYPE_CHECKING:
    from app.modules.productos.models import Producto

class Categoria(Base, table = True):
    
    __tablename__ = "Categoria"

    nombre: str = Field(min_length=2, max_length=100, unique = True, nullable = False)

    descripcion: str = Field(nullable = False)

    imagen_url: Optional[str] = Field(nullable = True)

    parent_id: Optional[int] = Field(
        default = None,
        sa_column = Column(
            Integer,
            ForeignKey("Categoria.id", ondelete="SET NULL"),
            nullable = True
        )
    )

    productos: List["Producto"] = Relationship(back_populates = "categorias", link_model = ProductoCategoria)