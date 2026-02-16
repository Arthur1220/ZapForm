"""
Sistema de Logging Limpo e Organizado
"""
import logging
import sys
from datetime import datetime

# Códigos de cores ANSI
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Cores principais
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    
    # Cores de fundo
    BG_RED = "\033[101m"
    BG_GREEN = "\033[102m"
    BG_YELLOW = "\033[103m"


class CleanFormatter(logging.Formatter):
    """Formatter customizado com cores e formato limpo"""
    
    FORMATS = {
        logging.DEBUG: Colors.CYAN + "🐛 DEBUG" + Colors.RESET + "    %(message)s",
        logging.INFO: Colors.BLUE + "ℹ️  INFO" + Colors.RESET + "     %(message)s",
        logging.WARNING: Colors.YELLOW + "⚠️  WARNING" + Colors.RESET + "  %(message)s",
        logging.ERROR: Colors.RED + "❌ ERROR" + Colors.RESET + "    %(message)s",
        logging.CRITICAL: Colors.BG_RED + Colors.WHITE + "💥 CRITICAL" + Colors.RESET + " %(message)s",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_clean_logging(level=logging.INFO):
    """Configura logging limpo para a aplicação"""
    
    # Remove handlers existentes
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Handler para console com formato limpo
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CleanFormatter())
    
    # Configura logger root
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # SILENCIA COMPLETAMENTE SQLAlchemy e Uvicorn
    logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.engine.Engine").setLevel(logging.ERROR)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.ERROR)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    
    return root_logger


# Logger específico para o ZapForm
logger = logging.getLogger("zapform")


def log_startup():
    """Log de inicialização"""
    print("\n" + "="*60)
    print(Colors.GREEN + Colors.BOLD + "🚀 ZapForm iniciando..." + Colors.RESET)
    print("="*60 + "\n")


def log_webhook_received(phone: str, name: str, message_type: str):
    """Log quando recebe webhook"""
    print("\n" + Colors.CYAN + "─"*60 + Colors.RESET)
    logger.info(f"📨 Webhook recebido de {Colors.BOLD}{name}{Colors.RESET} ({phone})")
    logger.info(f"   Tipo: {message_type}")


def log_processing_start(phone: str, text: str):
    """Log início do processamento"""
    print(Colors.BLUE + "─"*60 + Colors.RESET)
    logger.info(f"⚙️  Processando: {Colors.BOLD}{text[:50]}{Colors.RESET}")


def log_step(step_number: int, step_name: str, status: str = "ok"):
    """Log de cada passo"""
    icons = {"ok": "✓", "skip": "⊘", "error": "✗"}
    colors = {"ok": Colors.GREEN, "skip": Colors.YELLOW, "error": Colors.RED}
    
    icon = icons.get(status, "•")
    color = colors.get(status, Colors.WHITE)
    
    print(f"  {color}{icon}{Colors.RESET} {step_number}. {step_name}")


def log_step_detail(detail: str, indent: int = 6):
    """Log de detalhe de um passo"""
    print(" " * indent + Colors.CYAN + detail + Colors.RESET)


def log_data_collected(field_name: str, value: str):
    """Log quando coleta um dado"""
    logger.info(f"   {Colors.GREEN}✓{Colors.RESET} {field_name}: {Colors.BOLD}{value}{Colors.RESET}")


def log_missing_fields(fields: list):
    """Log de campos faltantes"""
    if fields:
        logger.info(f"   {Colors.YELLOW}⏳{Colors.RESET} Faltam: {', '.join(fields)}")
    else:
        logger.info(f"   {Colors.GREEN}✓{Colors.RESET} Todos os campos preenchidos!")


def log_completion():
    """Log quando completa cadastro"""
    print("\n" + Colors.GREEN + "="*60)
    print(Colors.GREEN + Colors.BOLD + "🎉 Cadastro completo!" + Colors.RESET)
    print(Colors.GREEN + "="*60 + Colors.RESET + "\n")


def log_error_summary(error_msg: str):
    """Log de erro resumido"""
    print(Colors.RED + "─"*60 + Colors.RESET)
    logger.error(f"Erro: {error_msg}")
    print(Colors.RED + "─"*60 + Colors.RESET + "\n")


def log_success_summary(collected: int, missing: int):
    """Log de resumo de sucesso"""
    print(Colors.BLUE + "─"*60 + Colors.RESET)
    logger.info(f"📊 Resumo: {Colors.GREEN}{collected} coletados{Colors.RESET}, "
               f"{Colors.YELLOW}{missing} faltantes{Colors.RESET}")
    print(Colors.CYAN + "─"*60 + Colors.RESET + "\n")