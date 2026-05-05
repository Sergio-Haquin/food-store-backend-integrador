from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.core.database import get_session
from app.modules.ingredientes.schemas import IngredienteCreate, IngredienteUpdate, IngredientePublic, IngredienteList
from app.modules.ingredientes.service import IngredienteService

router = APIRouter()

def get_ingrediente_service(session: Session = Depends(get_session)) -> IngredienteService:

    return IngredienteService(session)

@router.get(
    "/",
    response_model = IngredienteList,
    summary = "Obtener una lista de ingredientes disponibles"
)
def get_ingredientes(
    offset: int = Query(default = 0, ge = 0),
    limit: int = Query(default = 20, ge = 1, le = 100),
    svc: IngredienteService = Depends(get_ingrediente_service)
) -> IngredienteList:
    
    return svc.get_all(offset = offset, limit = limit)

@router.post(
    "/",
    response_model = IngredientePublic,
    status_code = status.HTTP_201_CREATED,
    summary = "Crear un nuevo ingrediente"
)
def create_ingrediente(data: IngredienteCreate, svc: IngredienteService = Depends(get_ingrediente_service)) -> IngredientePublic:
    
    return svc.create_ingrediente(data)

@router.get(
    "/{ingrediente_id}",
    response_model = IngredientePublic,
    summary = "Obtener un ingrediente por su ID"
)
def get_ingrediente(
    ingrediente_id: int,
    svc: IngredienteService = Depends(get_ingrediente_service)
) -> IngredientePublic:
    
    return svc.get_by_id(ingrediente_id)

@router.patch(
    "/{ingrediente_id}",
    response_model = IngredientePublic,
    summary = "Actualizar un ingrediente por su ID"
)
def update_ingrediente(
    ingrediente_id: int,
    data: IngredienteUpdate,
    svc: IngredienteService = Depends(get_ingrediente_service)
) -> IngredientePublic:
    
    return svc.update_ingrediente(ingrediente_id, data)

@router.delete(
    "/{ingrediente_id}",
    summary= "Eliminar un ingrediente por su ID"
)
def delete_ingrediente(
    ingrediente_id: int,
    svc: IngredienteService = Depends(get_ingrediente_service)
) -> None:
    
    return svc.delete_ingrediente(ingrediente_id)
