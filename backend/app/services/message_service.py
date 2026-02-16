"""
Message Service - Gerenciamento de mensagens.
Responsável por salvar e buscar o histórico de conversa.
"""
import logging
from typing import List
from sqlmodel import Session, select
from app.models.message import Message

logger = logging.getLogger(__name__)


def save_message(
    session: Session,
    session_id: int,
    role: str,
    content: str
) -> Message:
    """
    Salva uma mensagem no histórico da sessão.
    
    Args:
        session: Sessão do banco de dados
        session_id: ID da sessão
        role: Papel ("user" ou "model")
        content: Conteúdo da mensagem
        
    Returns:
        Message: Mensagem salva
        
    Example:
        >>> save_message(session, 1, "user", "Olá!")
        >>> save_message(session, 1, "model", "Olá! Como posso ajudar?")
    """
    message = Message(
        session_id=session_id,
        role=role,
        content=content
    )
    
    session.add(message)
    session.commit()
    session.refresh(message)
    
    logger.debug(f"💬 Mensagem salva: [{role}] {content[:50]}...")
    
    return message


def get_recent_messages(
    session: Session,
    session_id: int,
    limit: int = 10
) -> List[Message]:
    """
    Busca as mensagens mais recentes de uma sessão.
    
    Args:
        session: Sessão do banco de dados
        session_id: ID da sessão
        limit: Número máximo de mensagens a retornar
        
    Returns:
        List[Message]: Lista de mensagens ordenadas por timestamp (mais antigas primeiro)
        
    Example:
        >>> messages = get_recent_messages(session, 1, limit=5)
        >>> for msg in messages:
        ...     print(f"[{msg.role}]: {msg.content}")
    """
    statement = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    
    messages = session.exec(statement).all()
    
    # Reverter ordem para ficar cronológica (mais antiga primeiro)
    messages.reverse()
    
    logger.info(f"📜 Buscadas {len(messages)} mensagens da sessão {session_id}")
    
    return messages


def get_all_messages(session: Session, session_id: int) -> List[Message]:
    """
    Busca TODAS as mensagens de uma sessão.
    
    Args:
        session: Sessão do banco de dados
        session_id: ID da sessão
        
    Returns:
        List[Message]: Lista completa de mensagens ordenadas cronologicamente
    """
    statement = (
        select(Message)
        .where(Message.session_id == session_id)
        .order_by(Message.timestamp)
    )
    
    messages = session.exec(statement).all()
    
    logger.info(f"📜 Total de mensagens na sessão {session_id}: {len(messages)}")
    
    return messages


def format_messages_for_context(messages: List[Message]) -> str:
    """
    Formata mensagens em texto para usar como contexto na IA.
    
    Args:
        messages: Lista de mensagens
        
    Returns:
        str: Mensagens formatadas como texto
        
    Example:
        >>> formatted = format_messages_for_context(messages)
        >>> print(formatted)
        User: Olá!
        Assistant: Olá! Como posso ajudar?
        User: Quero me cadastrar
    """
    formatted = []
    
    for msg in messages:
        role_name = "User" if msg.role == "user" else "Assistant"
        formatted.append(f"{role_name}: {msg.content}")
    
    return "\n".join(formatted)