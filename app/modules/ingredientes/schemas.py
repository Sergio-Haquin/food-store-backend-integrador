from typing import Optional, List
from sqlmodel import SQLModel, Field

class IngredienteList(SQLModel):
    data: List["IngredientePublic"]
    total: int

class IngredienteCreate(SQLModel):

    nombre: str = Field(min_length = 2, max_length = 100)

    descripcion: Optional[str] = Field(default = None, max_length = 255)

    es_alergeno: bool = Field(default = False)

class IngredienteUpdate(SQLModel):

    nombre: Optional[str] = Field(default = None, min_length = 2, max_length = 100)

    descripcion: Optional[str] = Field(default = None, max_length = 255)

    es_alergeno: Optional[bool] = None

class IngredientePublic(SQLModel):

    id: int

    nombre: str

    descripcion: Optional[str]

    es_alergeno: bool
