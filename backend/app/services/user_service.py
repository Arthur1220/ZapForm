"""
User Service - Gerenciamento de usuários.
Responsável por criar, buscar e atualizar usuários do sistema.
"""
import logging
from sqlmodel import Session, select
from app.models.user import User

logger = logging.getLogger(__name__)


def get_or_create_user(session: Session, phone_number: str, name: str) -> User:
    """
    Busca um usuário pelo telefone ou cria um novo se não existir.
    
    Args:
        session: Sessão do banco de dados
        phone_number: Número de telefone no formato internacional (ex: 5511999999999)
        name: Nome do usuário
        
    Returns:
        User: Usuário encontrado ou recém-criado
        
    Example:
        >>> user = get_or_create_user(session, "5511999999999", "João Silva")
        >>> print(user.id, user.name)
        1 João Silva
    """
    # Buscar usuário existente
    statement = select(User).where(User.phone_number == phone_number)
    user = session.exec(statement).first()
    
    if user:
        logger.info(f"👤 Usuário existente encontrado: {user.name} (ID: {user.id})")
        
        # Atualizar nome se mudou
        if user.name != name:
            logger.info(f"📝 Atualizando nome de '{user.name}' para '{name}'")
            user.name = name
            session.add(user)
            session.commit()
            session.refresh(user)
        
        return user
    
    # Criar novo usuário
    user = User(phone_number=phone_number, name=name)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    logger.info(f"✨ Novo usuário criado: {user.name} (ID: {user.id}, Tel: {phone_number})")
    
    return user


def get_user_by_phone(session: Session, phone_number: str) -> User | None:
    """
    Busca um usuário pelo número de telefone.
    
    Args:
        session: Sessão do banco de dados
        phone_number: Número de telefone no formato internacional
        
    Returns:
        User | None: Usuário encontrado ou None
    """
    statement = select(User).where(User.phone_number == phone_number)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """
    Busca um usuário pelo ID.
    
    Args:
        session: Sessão do banco de dados
        user_id: ID do usuário
        
    Returns:
        User | None: Usuário encontrado ou None
    """
    return session.get(User, user_id)