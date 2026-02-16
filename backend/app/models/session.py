"""
Modelo Session - Representa uma sessão de coleta de dados.
Cada sessão armazena o progresso da entrevista com um usuário.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel, Column, JSON


class Session(SQLModel, table=True):
    """
    Tabela de sessões de coleta de dados.
    Cada sessão rastreia o progresso de uma entrevista com um usuário.
    
    Attributes:
        id: ID único da sessão
        user_id: ID do usuário (Foreign Key)
        status: Status da sessão (OPEN, COMPLETED, CLOSED)
        form_data: Dados coletados em formato JSON
        created_at: Data de início da coleta
        updated_at: Data da última interação
    """
    __tablename__ = "sessions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        description="ID do usuário dono desta sessão"
    )
    status: str = Field(
        default="OPEN",
        description="Status da sessão: OPEN, COMPLETED ou CLOSED"
    )
    form_data: Dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Dados coletados do formulário em formato JSON"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data de início da sessão"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data da última atualização"
    )
    
    # Relacionamento com User
    # user: Optional["User"] = Relationship(back_populates="sessions")
    # messages: list["Message"] = Relationship(back_populates="session")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "status": "OPEN",
                "form_data": {
                    "nome": "João Silva",
                    "idade": 30
                },
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:35:00"
            }
        }