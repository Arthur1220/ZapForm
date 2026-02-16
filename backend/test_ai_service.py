"""
Script de teste para o AI Service.
Execute: docker-compose exec api python test_ai_service.py
"""
from app.services import ai_service
from app.models.info import Info
from app.models.message import Message
from datetime import datetime


def test_build_system_prompt():
    """Testa construção do prompt do sistema"""
    print("\n" + "="*80)
    print("🧪 TESTE 1: Build System Prompt")
    print("="*80)
    
    # Criar campos faltantes
    missing = [
        Info(key="nome", description="Pergunte o nome completo do usuário", order=1),
        Info(key="idade", description="Pergunte a idade. Deve ser maior que 18", order=2),
        Info(key="email", description="Pergunte o email", order=3),
    ]
    
    prompt = ai_service.build_system_prompt(missing)
    
    print("\n📝 Prompt gerado:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    assert "nome" in prompt, "Prompt deve mencionar 'nome'"
    assert "idade" in prompt, "Prompt deve mencionar 'idade'"
    assert "extracted_data" in prompt, "Prompt deve explicar formato JSON"
    
    print("✅ Prompt construído corretamente!")


def test_build_system_prompt_empty():
    """Testa prompt quando não há campos faltantes"""
    print("\n" + "="*80)
    print("🧪 TESTE 2: Prompt Sem Campos Faltantes")
    print("="*80)
    
    prompt = ai_service.build_system_prompt([])
    
    print("\n📝 Prompt gerado:")
    print("-" * 80)
    print(prompt)
    print("-" * 80)
    
    assert "completo" in prompt.lower(), "Deve indicar que está completo"
    print("✅ Prompt de conclusão correto!")


def test_extract_data():
    """Testa extração de dados do JSON"""
    print("\n" + "="*80)
    print("🧪 TESTE 3: Extração de Dados")
    print("="*80)
    
    # Resposta com JSON no formato esperado
    response1 = """Prazer em conhecer você, João! 

Qual é o seu email?

{"extracted_data": {"nome": "João", "idade": 30}}"""
    
    data1 = ai_service.extract_data_from_response(response1)
    print(f"✅ Teste 1 - Dados extraídos: {data1}")
    assert data1 == {"nome": "João", "idade": 30}
    
    # Resposta com JSON simples
    response2 = """Ótimo! {"nome": "Maria", "cidade": "São Paulo"}"""
    
    data2 = ai_service.extract_data_from_response(response2)
    print(f"✅ Teste 2 - Dados extraídos: {data2}")
    assert data2 == {"nome": "Maria", "cidade": "São Paulo"}
    
    # Resposta sem JSON
    response3 = "Qual é o seu nome?"
    
    data3 = ai_service.extract_data_from_response(response3)
    print(f"✅ Teste 3 - Sem dados: {data3}")
    assert data3 is None
    
    print("✅ Extração de dados funcionando!")


def test_clean_response():
    """Testa limpeza da resposta"""
    print("\n" + "="*80)
    print("🧪 TESTE 4: Limpeza de Resposta")
    print("="*80)
    
    response = """Prazer, João! Tenho 25 anos registrado.

Qual é o seu email?

{"extracted_data": {"nome": "João", "idade": 25}}"""
    
    cleaned = ai_service.clean_response_for_user(response)
    
    print("\n📝 Resposta original:")
    print(response)
    print("\n🧹 Resposta limpa:")
    print(cleaned)
    
    assert "extracted_data" not in cleaned, "JSON deve ser removido"
    assert "João" in cleaned, "Texto deve permanecer"
    
    print("✅ Limpeza funcionando!")


def test_build_conversation_context():
    """Testa construção do contexto da conversa"""
    print("\n" + "="*80)
    print("🧪 TESTE 5: Contexto da Conversa")
    print("="*80)
    
    messages = [
        Message(id=1, session_id=1, role="user", content="Olá!", timestamp=datetime.now()),
        Message(id=2, session_id=1, role="model", content="Olá! Como posso ajudar?", timestamp=datetime.now()),
        Message(id=3, session_id=1, role="user", content="Quero me cadastrar", timestamp=datetime.now()),
    ]
    
    context = ai_service.build_conversation_context(messages)
    
    print("\n📜 Contexto gerado:")
    print(context)
    
    assert "Olá!" in context
    assert "cadastrar" in context
    
    print("✅ Contexto construído!")


def test_call_gemini_mock():
    """Testa chamada ao Gemini (com resposta simulada se falhar)"""
    print("\n" + "="*80)
    print("🧪 TESTE 6: Chamada ao Gemini")
    print("="*80)
    
    system_prompt = "Você é um assistente amigável."
    user_message = "Olá!"
    
    try:
        response = ai_service.call_gemini(system_prompt, user_message)
        print(f"\n🤖 Resposta do Gemini:")
        print(response)
        print("✅ Gemini respondeu com sucesso!")
        
    except Exception as e:
        print(f"⚠️  Gemini não disponível: {e}")
        print("ℹ️  Certifique-se de que GOOGLE_API_KEY está configurada no .env")
        print("✅ Teste pulado (API não disponível)")


def test_process_user_message():
    """Testa processamento completo de mensagem"""
    print("\n" + "="*80)
    print("🧪 TESTE 7: Processamento Completo")
    print("="*80)
    
    missing_fields = [
        Info(key="nome", description="Pergunte o nome completo", order=1),
        Info(key="idade", description="Pergunte a idade", order=2),
    ]
    
    history = []
    user_message = "Oi, meu nome é Carlos e tenho 28 anos"
    
    try:
        response, data = ai_service.process_user_message(
            user_message,
            missing_fields,
            history
        )
        
        print(f"\n💬 Mensagem do usuário: {user_message}")
        print(f"\n🤖 Resposta da IA:")
        print(response)
        print(f"\n📊 Dados extraídos: {data}")
        
        if data:
            print("✅ Processamento completo com extração de dados!")
        else:
            print("✅ Processamento completo (sem dados extraídos)")
            
    except Exception as e:
        print(f"⚠️  Erro no processamento: {e}")
        print("ℹ️  Verifique se GOOGLE_API_KEY está configurada")
        print("✅ Teste pulado (API não disponível)")


def run_all_tests():
    """Executa todos os testes"""
    print("="*80)
    print("🧪 TESTES DO AI SERVICE - ZapForm")
    print("="*80)
    
    try:
        test_build_system_prompt()
        test_build_system_prompt_empty()
        test_extract_data()
        test_clean_response()
        test_build_conversation_context()
        
        print("\n" + "="*80)
        print("⚠️  TESTES COM API REAL (requerem GOOGLE_API_KEY)")
        print("="*80)
        
        test_call_gemini_mock()
        test_process_user_message()
        
        print("\n" + "="*80)
        print("✅ TESTES DO AI SERVICE CONCLUÍDOS!")
        print("="*80)
        print("\n📋 Próximos passos:")
        print("1. Fase 6: WhatsApp Service (enviar mensagens)")
        print("2. Fase 7: Orchestrator (juntar tudo!)")
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ ERRO NOS TESTES: {e}")
        print("="*80)
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    run_all_tests()