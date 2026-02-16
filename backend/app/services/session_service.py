"""
Session Service - Gerencia sessões de coleta de dados
"""
from sqlmodel import Session, select
from app.models import Session as SessionModel, Info


def calculate_missing_fields(db: Session, session: SessionModel) -> set:
    """
    Calcula quais campos ainda faltam ser preenchidos.
    
    CORREÇÃO: Retorna set de STRINGS (nomes dos campos), não objetos Info
    """
    # Buscar todos os campos obrigatórios
    stmt = select(Info).order_by(Info.order)
    required_infos = db.exec(stmt).all()
    
    # Extrair apenas as KEYS (strings) dos campos obrigatórios
    required_fields = {info.key for info in required_infos}
    
    # Campos já preenchidos
    filled_fields = set(session.form_data.keys()) if session.form_data else set()
    
    # Retornar apenas as STRINGS dos campos faltantes
    missing = required_fields - filled_fields
    
    return missing


def get_or_create_open_session(db: Session, user_id: int) -> SessionModel:
    """Busca sessão aberta ou cria nova"""
    stmt = select(SessionModel).where(
        SessionModel.user_id == user_id,
        SessionModel.status == "OPEN"
    ).order_by(SessionModel.created_at.desc())
    
    session = db.exec(stmt).first()
    
    if not session:
        session = SessionModel(
            user_id=user_id,
            status="OPEN",
            form_data={}
        )
        db.add(session)
        db.commit()
        db.refresh(session)
    
    return session


def update_form_data(db: Session, session_id: int, new_data: dict) -> SessionModel:
    """Atualiza form_data da sessão"""
    session = db.get(SessionModel, session_id)
    
    if session:
        current_data = session.form_data or {}
        current_data.update(new_data)
        session.form_data = current_data
        
        db.add(session)
        db.commit()
        db.refresh(session)
    
    return session


def close_session(db: Session, session_id: int, status: str = "COMPLETED") -> SessionModel:
    """Fecha uma sessão"""
    session = db.get(SessionModel, session_id)
    
    if session:
        session.status = status
        db.add(session)
        db.commit()
        db.refresh(session)
    
    return session


def get_session_by_id(db: Session, session_id: int) -> SessionModel:
    """Busca sessão por ID"""
    return db.get(SessionModel, session_id)