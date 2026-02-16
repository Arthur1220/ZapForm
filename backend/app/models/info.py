"""
Modelo Info - Define os campos do formulário dinâmico.
Cada registro representa uma pergunta/informação que a IA deve coletar.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Info(SQLModel, table=True):
    """
    Tabela de configuração do formulário dinâmico.
    Define quais informações devem ser coletadas e como.
    
    Attributes:
        id: ID único do campo
        key: Chave única para identificar o campo no JSON (ex: "idade", "endereco")
        description: Instrução para a IA sobre como coletar este campo
        order: Ordem de prioridade da pergunta (menor = maior prioridade)
        created_at: Data e hora de criação do campo
    """
    __tablename__ = "infos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(
        unique=True,
        index=True,
        description="Chave única para o campo (ex: 'idade', 'endereco')"
    )
    description: str = Field(
        description="Instrução para a IA sobre como coletar este campo"
    )
    order: int = Field(
        default=0,
        description="Ordem de prioridade (menor número = maior prioridade)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data e hora de criação do campo"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "key": "idade",
                "description": "Pergunte a idade do usuário. Deve ser um número maior que 18.",
                "order": 2,
                "created_at": "2024-01-15T10:30:00"
            }
        }