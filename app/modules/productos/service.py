from fastapi import HTTPException, status
from sqlmodel import Session
from app.modules.productos.models import Producto
from app.modules.productos.schemas import ProductoCreate, ProductoUpdate, ProductoPublic, ProductoList
from app.modules.productos.unit_of_work import ProductoUnitOfWork


class ProductoService:

    def __init__(self,session: Session) -> None:

        self._session = session

    def _get_or_404(self, uow: ProductoUnitOfWork, producto_id: int) -> Producto:

        producto = uow.productos.get_by_id(producto_id)

        if not producto:
            
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Producto con id {producto_id} no encontrado"
            )
        
        return producto

    def create_producto(self, data: ProductoCreate) -> ProductoPublic:

        with ProductoUnitOfWork(self._session) as uow:

            producto = Producto(
                nombre=data.nombre,
                descripcion=data.descripcion,
                precio_base=data.precio_base,
                imagenes_url=data.imagenes_url,
                stock_cantidad=data.stock_cantidad,
                disponible=data.disponible,
            )
            uow.productos.add(producto)

            principales = [c for c in data.categorias if c.es_principal]
            if len(principales) > 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Solo puede haber una categoría principal por producto",
                )
            for cat_input in data.categorias:
                cat = uow.categorias.get_by_id(cat_input.categoria_id)
                if not cat:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Categoría {cat_input.categoria_id} no encontrada",
                    )
                uow.productos.add_categoria(producto.id, cat_input.categoria_id, cat_input.es_principal)

            for ing_input in data.ingredientes:
                ing = uow.ingredientes.get_by_id(ing_input.ingrediente_id)
                if not ing:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Ingrediente {ing_input.ingrediente_id} no encontrado",
                    )
                uow.productos.add_ingrediente(producto.id, ing_input.ingrediente_id, ing_input.es_removible)

            result = ProductoPublic.model_validate(producto)

        return result
    
    def get_all (self, offset: int = 0, limit: int = 20) -> ProductoList:

        with ProductoUnitOfWork(self._session) as uow:

            productos = uow.productos.get_actives(offset, limit)
            total = uow.productos.count()
            result = ProductoList(
                data = [ProductoPublic.model_validate(p) for p in productos], total = total
            )

        return result
    
    def get_by_id(self, producto_id: int) -> ProductoPublic:

        with ProductoUnitOfWork(self._session) as uow:

            producto = self._get_or_404(uow, producto_id)
            result = ProductoPublic.model_validate(producto)

        return result
    
    def update_producto(self, producto_id: int, data: ProductoUpdate) -> ProductoPublic:

        with ProductoUnitOfWork(self._session) as uow:

            producto = self._get_or_404(uow, producto_id)
            patch = data.model_dump(exclude_unset = True)

            for field, value in patch.items():

                setattr(producto, field, value)

            uow.productos.add(producto)
            result = ProductoPublic.model_validate(producto)

        return result
    
    def desactivar_producto(self, producto_id: int) -> None:

        with ProductoUnitOfWork(self._session) as uow:

            producto = self._get_or_404(uow, producto_id)
            producto.disponible = False
            uow.productos.add(producto)
            
    def activar_producto(self, producto_id: int) -> None:

        with ProductoUnitOfWork(self._session) as uow:

            producto = self._get_or_404(uow, producto_id)
            producto.disponible = True
            uow.productos.add(producto)

    def delete_producto(self, producto_id: int) -> None:

        with ProductoUnitOfWork(self._session) as uow:

            producto = self._get_or_404(uow, producto_id)
            producto.is_active = False
            uow.productos.add(producto)