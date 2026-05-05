
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.modules.categorias.models import Categoria
from app.modules.productos.models import Producto, ProductoCategoria, ProductoIngrediente


class ProductoRepository(BaseRepository[Producto]):

    def __init__(self, session: Session) -> None:

        super().__init__(session, Producto)

    def get_by_id(self, id: int) -> Producto | None:
        
        return self.session.exec(

            select(Producto).where(Producto.id == id)

        ).first()
    
    def get_actives(self, offset: int = 0, limit: int = 20) -> list[Producto]:

        return list(

            self.session.exec(

                select(Producto)
                .where(Producto.disponible,Producto.activo)
                .offset(offset)
                .limit(limit)
            
            ).all()

        )
    
    def get_active(self, id: int) -> Producto | None:

        return self.session.exec(

            select(Producto)
            .where(Producto.id == id, Producto.disponible & Producto.activo)

        ).first()

    def get_by_categoria(self, categoria_name: str, offset: int = 0, limit: int = 20) -> list[Producto]:

        return list(

            self.session.exec(

                select(Producto)
                .where(Producto.disponible & Producto.activo)
                .join(Producto.categorias)
                .where(Categoria.nombre == categoria_name)
                .offset(offset)
                .limit(limit)

            ).all()

        )
    
    def add_ingrediente(self, producto_id: int, ingrediente_id: int, es_removible: bool) -> ProductoIngrediente:

        link = ProductoIngrediente(

            producto_id=producto_id,
            ingrediente_id=ingrediente_id,
            es_removible=es_removible,

        )
        self.session.add(link)

        return link
    
    def add_categoria(self, producto_id: int, categoria_id: int, es_principal: bool) -> ProductoCategoria:

        link = ProductoCategoria(

            producto_id=producto_id,
            categoria_id=categoria_id,
            es_principal=es_principal

        )
        self.session.add(link)

        return link

    def count (self) -> int:

        return len(self.session.exec(select(Producto)).all())
