from fastapi import HTTPException, status
from sqlmodel import Session
from app.modules.categorias.models import Categoria
from app.modules.categorias.schemas import CategoriaCreate, CategoriaTree, CategoriaUpdate, CategoriaPublic, CategoriaList
from app.modules.categorias.unit_of_work import CategoriaUnitOfWork

class CategoriaService:

    def __init__(self, session: Session) -> None:

        self._session = session

    def _get_or_404(self, uow: CategoriaUnitOfWork, categoria_id: int) -> Categoria:

        categoria = uow.categorias.get_by_id(categoria_id)

        if not categoria:
            
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Categoria con id {categoria_id} no encontrada"
            )
        
        return categoria

    def _assert_name_unique(self, uow: CategoriaUnitOfWork, nombre: str) -> None:

        if uow.categorias.get_by_name(nombre):

            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"Categoria con nombre '{nombre}' ya existe"
            )
        
    def create_categoria(self, data: CategoriaCreate) -> CategoriaPublic:

        with CategoriaUnitOfWork(self._session) as uwo:

            self._assert_name_unique(uwo, data.nombre)
            categoria = Categoria.model_validate(data)
            uwo.categorias.add(categoria)
            result = CategoriaPublic.model_validate(categoria)

        return result
    
    def get_all(self, offset: int = 0, limit: int = 20) -> CategoriaList:

        with CategoriaUnitOfWork(self._session) as uwo:

            categorias = uwo.categorias.get_all(offset, limit)
            total = uwo.categorias.count()
            result = CategoriaList(
                data = [CategoriaPublic.model_validate(c) for c in categorias], total = total
            )

        return result
    
    def get_by_id(self, categoria_id: int) -> CategoriaPublic:

        with CategoriaUnitOfWork(self._session) as uwo:

            categoria = self._get_or_404(uwo, categoria_id)
            result = CategoriaPublic.model_validate(categoria)

        return result
    
    def update_categoria(self, categoria_id: int, data: CategoriaUpdate) -> CategoriaPublic:

        with CategoriaUnitOfWork(self._session) as uwo:

            categoria = self._get_or_404(uwo, categoria_id)

            if data.nombre and data.nombre != categoria.nombre:
                self._assert_name_unique(uwo, data.nombre)

            patch = data.model_dump(exclude_unset = True)
            for field, value in patch.items():
                setattr(categoria, field, value)

            uwo.categorias.add(categoria)
            result = CategoriaPublic.model_validate(categoria)

        return result
    
    def delete_categoria(self, categoria_id: int) -> None:

        with CategoriaUnitOfWork(self._session) as uwo:

            categoria = self._get_or_404(uwo, categoria_id)
            categoria.is_active = False
            uwo.categorias.add(categoria)

    def get_tree(self) -> list[CategoriaTree]:

        with CategoriaUnitOfWork(self._session) as uow:

            todas = uow.categorias.get_all_active()

        return self._build_tree(todas)


    def _build_tree(categorias: list[Categoria]) -> list[CategoriaTree]:

        nodos = {
            cat.id: CategoriaTree(
                id=cat.id,
                nombre=cat.nombre
            )
            for cat in categorias
        }

        raices = []
        for cat in categorias:
            if cat.parent_id is None:
                raices.append(nodos[cat.id])
            else:
                padre = nodos.get(cat.parent_id)
                if padre:
                    padre.subcategorias.append(nodos[cat.id])

        return raices