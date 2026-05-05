from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.core.database import get_session
from app.modules.productos.schemas import ProductoCreate, ProductoUpdate, ProductoPublic, ProductoList
from app.modules.productos.service import ProductoService

router = APIRouter()

def get_producto_service(session: Session = Depends(get_session)) -> ProductoService:

    return ProductoService(session)

@router.post(
    "/",
    response_model = ProductoPublic,
    status_code = status.HTTP_201_CREATED,
    summary = "Crear un nuevo producto"
)
def create_producto(data: ProductoCreate,svc: ProductoService = Depends(get_producto_service)) -> ProductoPublic:
    
    return svc.create_producto(data)

@router.get(
    "/",
    response_model = ProductoList,
    summary = "Obtener una lista de productos disponibles"
)
def get_productos(
    offset: int = Query(default = 0, ge = 0),
    limit: int = Query(default = 20, ge = 1, le = 100),
    svc: ProductoService = Depends(get_producto_service)
) -> ProductoList:
    
    return svc.get_all(offset, limit)

@router.get(
    "/{producto_id}",
    response_model = ProductoPublic,
    summary = "Obtener un producto por su ID"
)
def get_producto(
    producto_id: int,
    svc: ProductoService = Depends(get_producto_service)
) -> ProductoPublic:
    
    return svc.get_by_id(producto_id)

@router.patch(
    "/{producto_id}",
    response_model = ProductoPublic,
    summary = "Actualizar un producto por su ID"
)
def update_producto(
    producto_id: int,
    data: ProductoUpdate,
    svc: ProductoService = Depends(get_producto_service)
) -> ProductoPublic:
    
    return svc.update_producto(producto_id, data)

@router.patch(
    "/{producto_id}/desactivar",
    summary = "Desactivar un producto por su ID"
)
def desactivar_producto(
    producto_id: int,
    svc: ProductoService = Depends(get_producto_service)
) -> None:
    
    svc.desactivar_producto(producto_id)

@router.patch(
    "/{producto_id}/activar",
    summary = "Activar un producto por su ID"
)
def activar_producto(
    producto_id: int,
    svc: ProductoService = Depends(get_producto_service)
) -> None:
    
    svc.activar_producto(producto_id)

@router.delete(
    "/{producto_id}",
    summary = "Eliminar un producto por su id"
)
def delete_producto(
    producto_id: int,
    svc: ProductoService = Depends(get_producto_service)
) -> None:
    svc.delete_producto(producto_id)