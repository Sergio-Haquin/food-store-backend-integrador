from typing import Optional, List
from sqlmodel import SQLModel, Field

class CategoriaCreate(SQLModel):
    nombre: str = Field(min_length = 2,max_length = 100)

    descripcion: str = Field(min_length = 2, max_length = 255)
    
    imagen_url: Optional[str] = Field(default = None, max_length = 255)

    parent_id: Optional[int] = None

class CategoriaUpdate(SQLModel):
    nombre: Optional[str] = Field(default = None, min_length = 2,max_length = 100)

    descripcion: Optional[str] = Field(default = None, min_length = 2, max_length = 255)
    
    imagen_url: Optional[str] = Field(default = None, max_length = 255)

    parent_id: Optional[int] = None

class CategoriaPublic(SQLModel):
    id: int

    nombre: str

    descripcion: str

    imagen_url: Optional[str]

class CategoriaList(SQLModel):

    data: List[CategoriaPublic]

    total: int

class CategoriaTree(SQLModel):
    id: int
    nombre: str
    subcategorias: List["CategoriaTree"] = []

CategoriaTree.model_rebuild()