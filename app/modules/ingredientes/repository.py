from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.modules.ingredientes.models import Ingrediente

class IngredienteRepository(BaseRepository[Ingrediente]):

    def __init__(self, session: Session) -> None:

        super().__init__(session, Ingrediente)

    def get_by_id(self, id: int) -> Ingrediente | None:
        
        return self.session.exec(

            select(Ingrediente)
            .where(Ingrediente.id == id)

        ).first()
    
    def get_all(self, offset: int = 0, limit: int = 20) -> list[Ingrediente]:

        return list(

            self.session.exec(

                select(Ingrediente)
                .offset(offset)
                .limit(limit)
            
            ).all()

        )
    
    def get_actives(self, offset: int = 0, limit: int = 20) -> list[Ingrediente]:

        return list(

            self.session.exec(

                select(Ingrediente)
                .where(Ingrediente.activo)
                .offset(offset)
                .limit(limit)

            ).all()

        )
    
    def get_no_alergenos(self, offset: int = 0, limit: int = 20) -> list[Ingrediente]:

        return list(

            self.session.exec(

                select(Ingrediente)
                .where(Ingrediente.es_alergeno == False & Ingrediente.activo)
                .offset(offset)
                .limit(limit) 
            
            ).all()

        )