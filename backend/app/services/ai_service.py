"""
AI Service - Integração com Google Gemini.
Responsável por construir prompts, chamar a IA e processar respostas.
"""
import logging
import json
import re
from typing import Dict, Any, List, Optional
import google.generativeai as genai

from app.core.config import settings
from app.models.info import Info
from app.models.message import Message

logger = logging.getLogger(__name__)

# Configurar Gemini
genai.configure(api_key=settings.google_api_key)


def build_system_prompt(missing_fields: List[Info]) -> str:
    """
    Constrói o prompt do sistema com instruções dinâmicas baseadas nos campos faltantes.
    
    Args:
        missing_fields: Lista de campos que ainda precisam ser coletados
        
    Returns:
        str: Prompt do sistema
    """
    if not missing_fields:
        return """Você é um assistente virtual amigável e prestativo.
Todos os dados do usuário já foram coletados.
Agradeça ao usuário e informe que o cadastro está completo."""
    
    # Construir lista de campos faltantes com instruções
    fields_list = []
    for field in missing_fields[:3]:  # Mostrar apenas os 3 próximos
        fields_list.append(f"- {field.key}: {field.description}")
    
    fields_text = "\n".join(fields_list)
    
    prompt = f"""Você é um assistente virtual amigável que está coletando informações de um usuário via WhatsApp.

CAMPOS QUE VOCÊ PRECISA COLETAR (em ordem de prioridade):
{fields_text}

REGRAS IMPORTANTES:
1. Pergunte APENAS UM campo por vez
2. Seja natural, amigável e conversacional
3. Se o usuário fornecer informações, extraia-as
4. Use linguagem simples e direta (é WhatsApp!)
5. Não use markdown, formatação especial ou emojis em excesso

FORMATO DE RESPOSTA:
Quando extrair uma informação, inclua no final da sua resposta um JSON com os dados:
{{
  "extracted_data": {{
    "nome_do_campo": "valor"
  }}
}}

EXEMPLO:
User: "Meu nome é João e tenho 25 anos"
Assistant: Prazer em conhecer você, João! Vejo que você tem 25 anos. 

Agora, qual é o seu email?

{{"extracted_data": {{"nome": "João", "idade": 25}}}}

Comece perguntando o primeiro campo da lista acima de forma natural e amigável."""
    
    return prompt


def build_conversation_context(messages: List[Message]) -> str:
    """
    Constrói o contexto da conversa a partir do histórico.
    
    Args:
        messages: Lista de mensagens anteriores
        
    Returns:
        str: Contexto formatado
    """
    if not messages:
        return "Esta é a primeira mensagem do usuário."
    
    context_lines = []
    for msg in messages[-5:]:  # Últimas 5 mensagens
        role = "Usuário" if msg.role == "user" else "Assistente"
        context_lines.append(f"{role}: {msg.content}")
    
    return "\n".join(context_lines)


def call_gemini(
    system_prompt: str,
    user_message: str,
    conversation_context: str = ""
) -> str:
    """
    Chama o Google Gemini para processar a mensagem.
    
    Args:
        system_prompt: Prompt do sistema com instruções
        user_message: Mensagem do usuário
        conversation_context: Contexto da conversa anterior
        
    Returns:
        str: Resposta da IA
    """
    try:
        # Configurar modelo
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Construir prompt completo
        full_prompt = f"""{system_prompt}

CONTEXTO DA CONVERSA:
{conversation_context}

NOVA MENSAGEM DO USUÁRIO:
{user_message}

Responda de forma natural e amigável. Se extrair dados, inclua o JSON no final."""
        
        logger.info("🤖 Chamando Gemini...")
        logger.debug(f"Prompt: {full_prompt[:200]}...")
        
        # Gerar resposta
        response = model.generate_content(full_prompt)
        
        ai_response = response.text
        logger.info(f"✅ Gemini respondeu: {ai_response[:100]}...")
        
        return ai_response
        
    except Exception as e:
        logger.error(f"❌ Erro ao chamar Gemini: {e}")
        # Resposta de fallback
        return "Desculpe, tive um problema técnico. Pode repetir sua mensagem?"


def extract_data_from_response(ai_response: str) -> Optional[Dict[str, Any]]:
    """
    Extrai dados estruturados da resposta da IA.
    
    A IA pode retornar um JSON no formato:
    {"extracted_data": {"nome": "João", "idade": 25}}
    
    Args:
        ai_response: Resposta completa da IA
        
    Returns:
        Dict[str, Any] | None: Dados extraídos ou None
    """
    try:
        # Procurar por JSON na resposta
        # Padrão: {"extracted_data": {...}}
        json_match = re.search(r'\{[^}]*"extracted_data"[^}]*\{[^}]+\}[^}]*\}', ai_response, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            logger.debug(f"JSON encontrado: {json_str}")
            
            data = json.loads(json_str)
            extracted = data.get("extracted_data", {})
            
            if extracted:
                logger.info(f"📊 Dados extraídos: {extracted}")
                return extracted
        
        # Tentar encontrar JSON simples sem wrapper
        json_match = re.search(r'\{[^{}]+\}', ai_response)
        if json_match:
            json_str = json_match.group(0)
            logger.debug(f"JSON simples encontrado: {json_str}")
            
            data = json.loads(json_str)
            # Se não tem chave "extracted_data", assume que o JSON inteiro são os dados
            if "extracted_data" not in data:
                logger.info(f"📊 Dados extraídos (formato simples): {data}")
                return data
        
        logger.info("ℹ️  Nenhum dado estruturado encontrado na resposta")
        return None
        
    except json.JSONDecodeError as e:
        logger.warning(f"⚠️  Erro ao fazer parse do JSON: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Erro ao extrair dados: {e}")
        return None


def clean_response_for_user(ai_response: str) -> str:
    """
    Remove o JSON da resposta antes de enviar ao usuário.
    
    Args:
        ai_response: Resposta completa da IA (pode conter JSON)
        
    Returns:
        str: Resposta limpa apenas com o texto
    """
    # Remover JSON do final
    cleaned = re.sub(r'\{[^}]*"extracted_data"[^}]*\{[^}]+\}[^}]*\}', '', ai_response, flags=re.DOTALL)
    
    # Remover JSON simples
    cleaned = re.sub(r'\{[^{}]+\}', '', cleaned)
    
    # Remover linhas vazias extras
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    
    # Remover espaços no início e fim
    cleaned = cleaned.strip()
    
    return cleaned


def process_user_message(
    user_message: str,
    missing_fields: List[Info],
    conversation_history: List[Message]
) -> tuple[str, Optional[Dict[str, Any]]]:
    """
    Processa uma mensagem do usuário de ponta a ponta.
    
    Args:
        user_message: Mensagem do usuário
        missing_fields: Campos que ainda faltam coletar
        conversation_history: Histórico da conversa
        
    Returns:
        tuple: (resposta_limpa_para_usuario, dados_extraidos)
        
    Example:
        >>> response, data = process_user_message(
        ...     "Meu nome é João",
        ...     [Info(key="nome", description="...")],
        ...     []
        ... )
        >>> print(response)
        "Prazer, João! Qual é a sua idade?"
        >>> print(data)
        {"nome": "João"}
    """
    # 1. Construir prompt do sistema
    system_prompt = build_system_prompt(missing_fields)
    
    # 2. Construir contexto da conversa
    context = build_conversation_context(conversation_history)
    
    # 3. Chamar Gemini
    ai_response = call_gemini(system_prompt, user_message, context)
    
    # 4. Extrair dados estruturados (se houver)
    extracted_data = extract_data_from_response(ai_response)
    
    # 5. Limpar resposta para o usuário (remover JSON)
    clean_response = clean_response_for_user(ai_response)
    
    logger.info(f"✅ Processamento completo - Dados extraídos: {bool(extracted_data)}")
    
    return clean_response, extracted_data