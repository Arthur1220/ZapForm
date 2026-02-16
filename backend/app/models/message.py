"""
Modelo Message - Representa mensagens trocadas durante a sessão.
Armazena o histórico de conversa entre usuário e IA.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """
    Tabela de mensagens trocadas durante a sessão.
    Mantém histórico completo da conversa.
    
    Attributes:
        id: ID único da mensagem
        session_id: ID da sessão (Foreign Key)
        role: Papel do emissor ('user' ou 'model')
        content: Conteúdo textual da mensagem
        timestamp: Data e hora do envio
    """
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(
        foreign_key="sessions.id",
        description="ID da sessão à qual esta mensagem pertence"
    )
    role: str = Field(
        description="Papel: 'user' para mensagens do usuário, 'model' para respostas da IA"
    )
    content: str = Field(
        description="Conteúdo textual da mensagem"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data e hora do envio da mensagem"
    )
    
    # Relacionamento com Session
    # session: Optional["Session"] = Relationship(back_populates="messages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "session_id": 1,
                "role": "user",
                "content": "Olá! Meu nome é João",
                "timestamp": "2024-01-15T10:30:00"
            }
        }