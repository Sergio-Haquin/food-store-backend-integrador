from fastapi import APIRouter, Depends, Query, status
from typing import List
from sqlmodel import Session
from app.core.database import get_session
from app.modules.categorias.schemas import CategoriaCreate, CategoriaPublic, CategoriaList, CategoriaTree, CategoriaUpdate
from app.modules.categorias.service import CategoriaService

router = APIRouter()

def get_categoria_service(session: Session = Depends(get_session)) -> CategoriaService:

    return CategoriaService(session)

@router.post(
    "/",
    response_model = CategoriaPublic,
    status_code = status.HTTP_201_CREATED,
    summary = "Crear una nueva categoria"
)
def create_categoria(data: CategoriaCreate, svc: CategoriaService = Depends(get_categoria_service)) -> CategoriaPublic:
    
    return svc.create_categoria(data)

@router.get(
    "/",
    response_model = CategoriaList,
    summary = "Obtener una lista de categorias disponibles"
)
def get_categorias(
    offset: int = Query(default = 0, ge = 0),
    limit: int = Query(default = 20, ge = 1, le = 100),
    svc: CategoriaService = Depends(get_categoria_service)
) -> CategoriaList:
    
    return svc.get_all(offset = offset, limit = limit)

@router.get(
    "/{categoria_id}",
    response_model = CategoriaPublic,
    summary = "Obtener una categoria por su ID"
)
def get_categoria(
    categoria_id: int,
    svc: CategoriaService = Depends(get_categoria_service)
) -> CategoriaPublic:
    
    return svc.get_by_id(categoria_id)

@router.get(
    "/tree",
    response_model = List[CategoriaTree],
    summary = "Obtener el árbol de categorías"
)
def get_tree(
    svc: CategoriaService = Depends(get_categoria_service)
) -> List[CategoriaTree]:
    
    return svc.get_tree()

@router.patch(
    "/{categoria_id}",
    response_model = CategoriaPublic,
    summary = "Actualizar una categoria por su ID"
)
def update_categoria(
    categoria_id: int,
    data: CategoriaUpdate,
    svc: CategoriaService = Depends(get_categoria_service)
) -> CategoriaPublic:
    
    return svc.update_categoria(categoria_id, data)

@router.delete(
    "/{categoria_id}",
    summary = "Eliminar una categoria por su ID"
)
def delete_categoria(
    categoria_id: int,
    svc: CategoriaService = Depends(get_categoria_service)
) -> None:
    
    return svc.delete_categoria(categoria_id)