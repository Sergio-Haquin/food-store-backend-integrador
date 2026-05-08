from fastapi import HTTPException, status
from sqlmodel import Session
from app.modules.ingredientes.models import Ingrediente
from app.modules.ingredientes.schemas import IngredienteCreate, IngredienteUpdate, IngredientePublic, IngredienteList
from app.modules.ingredientes.unit_of_work import IngredienteUnitOfWork

class IngredienteService:

    def __init__(self, session: Session) -> None:

        self._session = session

    def _get_or_404(self, uow: IngredienteUnitOfWork, ingrediente_id: int) -> Ingrediente:

        ingrediente = uow.ingredientes.get_by_id(ingrediente_id)

        if not ingrediente:
            
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Ingrediente con id {ingrediente_id} no encontrado"
            )
        
        return ingrediente
    
    def create_ingrediente(self, data: IngredienteCreate) -> IngredientePublic:

        with IngredienteUnitOfWork(self._session) as uow:
            
            ingrediente = Ingrediente.model_validate(data)
            uow.ingredientes.add(ingrediente)
            result = IngredientePublic.model_validate(ingrediente)

        return result
    
    def get_by_id(self, ingrediente_id: int) -> IngredientePublic:

        with IngredienteUnitOfWork(self._session) as uow:

            ingrediente = self._get_or_404(uow, ingrediente_id)
            result = IngredientePublic.model_validate(ingrediente)

        return result
    
    def get_all(self, offset: int = 0, limit: int = 20) -> IngredienteList:

        with IngredienteUnitOfWork(self._session) as uow:

            # Obtener total de ingredientes activos
            total = len(uow.ingredientes.get_all())
            
            # Obtener ingredientes con paginación
            ingredientes = uow.ingredientes.get_all()[offset : offset + limit]
            
            # Convertir a public
            result_data = [IngredientePublic.model_validate(i) for i in ingredientes]

        return IngredienteList(data=result_data, total=total)
    
    def update_ingrediente(self, ingrediente_id: int, data: IngredienteUpdate) -> IngredientePublic:

        with IngredienteUnitOfWork(self._session) as uow:

            ingrediente = self._get_or_404(uow, ingrediente_id)
            patch = data.model_dump(exclude_unset = True)
            for field, value in patch.items():

                setattr(ingrediente, field, value)

            uow.ingredientes.update(ingrediente)
            result = IngredientePublic.model_validate(ingrediente)

        return result
    
    def delete_ingrediente(self, ingrediente_id: int) -> None:

        with IngredienteUnitOfWork(self._session) as uow:

            ingrediente = self._get_or_404(uow, ingrediente_id)
            ingrediente.activo = False
            uow.ingredientes.add(ingrediente)