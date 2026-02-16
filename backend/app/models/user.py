"""
Modelo User - Representa os usuários do sistema.
Cada usuário é identificado pelo número de telefone do WhatsApp.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    """
    Tabela de usuários do sistema.
    
    Attributes:
        id: ID único do usuário (gerado automaticamente)
        phone_number: Número de telefone no formato internacional (ex: 5511999999999)
        name: Nome do usuário capturado do webhook ou inferido
        created_at: Data e hora de criação do registro
    """
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    phone_number: str = Field(
        unique=True, 
        index=True,
        description="Número de telefone no formato internacional (ex: 5511999999999)"
    )
    name: str = Field(
        description="Nome do usuário capturado do WhatsApp"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data e hora de criação do usuário"
    )
    
    # Relacionamento com Session (um usuário pode ter várias sessões)
    # sessions: list["Session"] = Relationship(back_populates="user")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "phone_number": "5511999999999",
                "name": "João Silva",
                "created_at": "2024-01-15T10:30:00"
            }
        }