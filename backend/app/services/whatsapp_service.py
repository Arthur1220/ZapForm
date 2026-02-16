"""
WhatsApp Service - Envio de mensagens via API do WhatsApp Business.
Responsável por enviar mensagens de texto para os usuários.
"""
import logging
import requests
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_text_message(phone_number: str, text: str) -> bool:
    """
    Envia uma mensagem de texto via WhatsApp Business API.
    
    Args:
        phone_number: Número de telefone no formato internacional (ex: 5511999999999)
        text: Texto da mensagem a enviar
        
    Returns:
        bool: True se enviou com sucesso, False caso contrário
        
    Example:
        >>> success = send_text_message("5511999999999", "Olá! Tudo bem?")
        >>> if success:
        ...     print("Mensagem enviada!")
    """
    try:
        url = settings.whatsapp_api_url
        
        headers = {
            "Authorization": f"Bearer {settings.whatsapp_api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {
                "body": text
            }
        }
        
        logger.info(f"📤 Enviando mensagem para {phone_number}")
        logger.debug(f"   Texto: {text[:100]}...")
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"✅ Mensagem enviada com sucesso para {phone_number}")
            return True
        else:
            logger.error(f"❌ Erro ao enviar mensagem: {response.status_code}")
            logger.error(f"   Resposta: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"⏱️  Timeout ao enviar mensagem para {phone_number}")
        return False
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Erro de rede ao enviar mensagem: {e}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Erro inesperado ao enviar mensagem: {e}")
        return False