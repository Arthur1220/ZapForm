"""
Orchestrator - Orquestra todo o fluxo de processamento de mensagens.
"""
from sqlmodel import Session

from app.core.database import engine
from app.core.logging_clean import (
    log_webhook_received, log_processing_start, log_step, log_step_detail,
    log_data_collected, log_missing_fields, log_completion, 
    log_error_summary, log_success_summary, logger
)
from app.services import user_service, session_service, message_service, ai_service, whatsapp_service


async def process_incoming_message(phone_number: str, user_name: str, message_text: str) -> None:
    """
    Processa uma mensagem recebida do WhatsApp de ponta a ponta.
    """
    
    log_processing_start(phone_number, message_text)
    
    with Session(engine) as db_session:
        try:
            # PASSO 1: Gerenciar usuário
            log_step(1, "Gerenciar usuário")
            user = user_service.get_or_create_user(db_session, phone_number, user_name)
            log_step_detail(f"ID: {user.id} | Nome: {user.name}")
            
            # PASSO 2: Gerenciar sessão  
            log_step(2, "Gerenciar sessão")
            session = session_service.get_or_create_open_session(db_session, user.id)
            collected = len(session.form_data) if session.form_data else 0
            log_step_detail(f"Sessão #{session.id} | {collected} campos coletados")
            
            # PASSO 3: Salvar mensagem do usuário
            log_step(3, "Salvar mensagem")
            message_service.save_message(db_session, session.id, "user", message_text)
            
            # PASSO 4: Calcular campos faltantes
            log_step(4, "Calcular campos faltantes")
            missing_fields = session_service.calculate_missing_fields(db_session, session)
            
            if not missing_fields:
                # Cadastro completo!
                log_step(5, "Cadastro completo!", "ok")
                
                session_service.close_session(db_session, session.id, "COMPLETED")
                
                completion_message = f"""🎉 Perfeito! Seu cadastro está completo!

Dados registrados:
- Nome: {session.form_data.get('nome')}
- Idade: {session.form_data.get('idade')} anos
- Email: {session.form_data.get('email')}
- Cidade: {session.form_data.get('cidade')}, {session.form_data.get('estado', '')}
- Profissão: {session.form_data.get('profissao')}
- Interesse: {session.form_data.get('interesse')}

Obrigado por fornecer todas as informações.
Em breve entraremos em contato!"""
                
                message_service.save_message(db_session, session.id, "model", completion_message)
                whatsapp_service.send_text_message(phone_number, completion_message)
                
                log_completion()
                return
            
            # Ainda faltam campos - CORREÇÃO AQUI!
            missing_field_names = [field.key for field in missing_fields]
            log_missing_fields(missing_field_names)
            
            # PASSO 5: Buscar histórico
            log_step(5, "Buscar histórico")
            history = message_service.get_recent_messages(db_session, session.id, limit=10)
            log_step_detail(f"{len(history)} mensagens")
            
            # PASSO 6: Processar com IA
            log_step(6, "Processar com IA")
            ai_response, extracted_data = ai_service.process_user_message(
                message_text, missing_fields, history
            )
            
            if not ai_response:
                log_step(6, "IA não respondeu", "error")
                log_error_summary("IA não gerou resposta")
                return
            
            # PASSO 7: Atualizar form_data
            if extracted_data:
                log_step(7, "Atualizar dados")
                session_service.update_form_data(db_session, session.id, extracted_data)
                
                # Mostrar dados coletados
                for field, value in extracted_data.items():
                    log_data_collected(field, str(value))
            else:
                log_step(7, "Nenhum dado novo", "skip")
            
            # PASSO 8: Salvar resposta da IA
            log_step(8, "Salvar resposta")
            message_service.save_message(db_session, session.id, "model", ai_response)
            
            # PASSO 9: Enviar resposta via WhatsApp
            log_step(9, "Enviar WhatsApp")
            success = whatsapp_service.send_text_message(phone_number, ai_response)
            
            if not success:
                log_step(9, "Falha ao enviar", "error")
                logger.warning("Mensagem não enviada, mas dados foram salvos")
            
            # Resumo final
            session_refresh = session_service.get_session_by_id(db_session, session.id)
            total_collected = len(session_refresh.form_data) if session_refresh.form_data else 0
            total_missing = len(session_service.calculate_missing_fields(db_session, session_refresh))
            
            log_success_summary(total_collected, total_missing)
            
        except Exception as e:
            log_error_summary(str(e))
            logger.exception("Erro detalhado:")
            raise