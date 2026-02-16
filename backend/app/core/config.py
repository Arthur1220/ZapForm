"""
Configurações da aplicação ZapForm.
Gerencia variáveis de ambiente e configurações globais.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente.
    
    Attributes:
        app_name: Nome da aplicação
        app_version: Versão da aplicação
        debug: Modo debug
        database_url: URL de conexão com PostgreSQL
        whatsapp_api_token: Token de acesso da API do WhatsApp
        whatsapp_phone_number_id: ID do número de telefone do WhatsApp Business
        whatsapp_verify_token: Token para verificação do webhook
        google_api_key: Chave da API do Google Gemini
    """
    
    # Configurações da aplicação
    app_name: str = "ZapForm"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Database
    database_url: str
    
    # WhatsApp Business API
    whatsapp_api_token: str
    whatsapp_phone_number_id: str
    whatsapp_verify_token: str
    
    # Google Gemini
    google_api_key: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def whatsapp_api_url(self) -> str:
        """URL base da API do WhatsApp Graph API v21.0"""
        return f"https://graph.facebook.com/v21.0/{self.whatsapp_phone_number_id}/messages"


# Instância global de configurações
settings = Settings()