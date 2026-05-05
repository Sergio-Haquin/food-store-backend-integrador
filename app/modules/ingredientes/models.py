from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from app.core.base import Base
from app.modules.productos.models import ProductoIngrediente

if TYPE_CHECKING:
    from app.modules.productos.models import Producto

class Ingrediente(Base, table = True):

    __tablename__ = "Ingrediente"

    nombre: str = Field(max_length = 100, nullable = False, unique = True)

    descripcion: Optional[str] = Field(default = None)

    es_alergeno: bool = Field(default = False, nullable = False)

    productos: List["Producto"] = Relationship(back_populates = "ingredientes", link_model = ProductoIngrediente)