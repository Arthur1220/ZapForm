"""
Configuração do banco de dados PostgreSQL com SQLModel.
Gerencia engine, sessões e criação de tabelas.
"""
from typing import Generator
from sqlmodel import Session, SQLModel, create_engine
from app.core.config import settings


# Criar engine do SQLAlchemy
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log de queries SQL em modo debug
    pool_pre_ping=True,   # Verifica conexão antes de usar
    pool_size=10,         # Tamanho do pool de conexões
    max_overflow=20       # Conexões extras permitidas
)


def create_db_and_tables() -> None:
    """
    Cria todas as tabelas no banco de dados.
    Deve ser chamado no startup da aplicação.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency para obter uma sessão do banco de dados.
    Utilizado com Depends() do FastAPI.
    
    Yields:
        Session: Sessão do SQLModel/SQLAlchemy
        
    Example:
```python
        @app.get("/users")
        def get_users(session: Session = Depends(get_session)):
            users = session.exec(select(User)).all()
            return users
```
    """
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()