"""
Router do Webhook do WhatsApp.
Recebe e processa mensagens da API do WhatsApp Business (Meta).
"""
from fastapi import APIRouter, Request, Query, HTTPException
from typing import Optional

from app.core.config import settings
from app.core.logging_clean import log_webhook_received, logger
from app.services.orchestrator import process_incoming_message

router = APIRouter()


@router.get("")
@router.head("")
async def verify_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token")
):
    """
    Endpoint de verificação do webhook do WhatsApp.
    O Meta envia GET/HEAD para verificar se o webhook é válido.
    """
    logger.info("🔐 Verificação de webhook")
    
    if not hub_mode or not hub_challenge or not hub_verify_token:
        raise HTTPException(status_code=400, detail="Parâmetros faltando")
    
    if hub_mode != "subscribe":
        raise HTTPException(status_code=403, detail="Modo inválido")
    
    if hub_verify_token != settings.whatsapp_verify_token:
        raise HTTPException(status_code=403, detail="Token inválido")
    
    logger.info("✅ Webhook verificado")
    return int(hub_challenge)


@router.post("")
async def receive_message(request: Request):
    """
    Endpoint para receber mensagens do WhatsApp.
    Integrado com o Orchestrator!
    """
    try:
        payload = await request.json()
        
        # Verificar estrutura do payload
        if "entry" not in payload:
            logger.warning("⚠️  Payload sem 'entry'")
            return {"status": "no_entry"}
        
        # Processar cada entrada
        for entry in payload["entry"]:
            if "changes" not in entry:
                continue
                
            for change in entry["changes"]:
                if "value" not in change:
                    continue
                    
                value = change["value"]
                
                # Ignorar status updates
                if "statuses" in value:
                    continue
                
                # Processar mensagens
                if "messages" in value and value["messages"]:
                    message = value["messages"][0]
                    
                    # Extrair dados
                    phone_number = message.get("from", "")
                    message_type = message.get("type", "unknown")
                    
                    # Buscar nome do contato
                    contacts = value.get("contacts", [])
                    user_name = "Usuário"
                    if contacts and len(contacts) > 0:
                        profile = contacts[0].get("profile", {})
                        user_name = profile.get("name", "Usuário")
                    
                    log_webhook_received(phone_number, user_name, message_type)
                    
                    # Processar apenas mensagens de texto
                    if message_type == "text":
                        text_content = message.get("text", {}).get("body", "")
                        
                        if text_content:
                            # CHAMA O ORCHESTRATOR!
                            await process_incoming_message(
                                phone_number=phone_number,
                                user_name=user_name,
                                message_text=text_content
                            )
                        else:
                            logger.warning("⚠️  Mensagem de texto vazia")
                    else:
                        logger.info(f"ℹ️  Tipo não suportado: {message_type}")
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"❌ Erro no webhook: {e}")
        logger.exception("Detalhes:")
        raise HTTPException(status_code=500, detail=str(e))