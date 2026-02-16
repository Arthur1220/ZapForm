"""
Script de teste para os Services de Negócio.
Execute: docker-compose exec api python test_services.py
"""
from sqlmodel import Session
from app.core.database import engine
from app.services import user_service, session_service, message_service


def test_user_service():
    """Testa o User Service"""
    print("\n" + "="*80)
    print("🧪 TESTE 1: User Service")
    print("="*80)
    
    with Session(engine) as session:
        # Criar usuário
        user1 = user_service.get_or_create_user(
            session, 
            "5511999999999", 
            "João Teste"
        )
        print(f"✅ Usuário criado: {user1.name} (ID: {user1.id})")
        
        # Buscar novamente (deve encontrar o existente)
        user2 = user_service.get_or_create_user(
            session,
            "5511999999999",
            "João Silva"  # Nome diferente
        )
        print(f"✅ Usuário encontrado e nome atualizado: {user2.name}")
        
        # Verificar que é o mesmo usuário
        assert user1.id == user2.id, "IDs devem ser iguais"
        print(f"✅ Mesmo usuário: ID {user1.id} = ID {user2.id}")
        
        # Buscar por telefone
        user3 = user_service.get_user_by_phone(session, "5511999999999")
        print(f"✅ Busca por telefone: {user3.name if user3 else 'Não encontrado'}")
        
        # Cleanup
        session.delete(user1)
        session.commit()
        print("✅ Cleanup concluído")


def test_session_service():
    """Testa o Session Service"""
    print("\n" + "="*80)
    print("🧪 TESTE 2: Session Service")
    print("="*80)
    
    with Session(engine) as session:
        # Criar usuário temporário
        user = user_service.get_or_create_user(
            session,
            "5511988888888",
            "Maria Teste"
        )
        
        # Criar sessão
        user_session = session_service.get_or_create_open_session(session, user.id)
        print(f"✅ Sessão criada: ID={user_session.id}, Status={user_session.status}")
        
        # Buscar novamente (deve encontrar a mesma)
        user_session2 = session_service.get_or_create_open_session(session, user.id)
        assert user_session.id == user_session2.id, "Deve ser a mesma sessão"
        print(f"✅ Mesma sessão encontrada: ID {user_session.id}")
        
        # Atualizar form_data
        updated = session_service.update_form_data(
            session,
            user_session.id,
            {"nome": "Maria", "idade": 25}
        )
        print(f"✅ Form data atualizado: {updated.form_data}")
        
        # Adicionar mais dados
        updated = session_service.update_form_data(
            session,
            user_session.id,
            {"cidade": "São Paulo"}
        )
        print(f"✅ Form data atualizado novamente: {updated.form_data}")
        
        # Calcular campos faltantes
        missing = session_service.calculate_missing_fields(session, updated)
        print(f"✅ Campos faltantes: {len(missing)}")
        for field in missing[:3]:
            print(f"   - {field.key}: {field.description[:50]}...")
        
        # Fechar sessão
        closed = session_service.close_session(session, user_session.id, "COMPLETED")
        print(f"✅ Sessão fechada: Status={closed.status}")
        
        # Cleanup
        session.delete(user_session)
        session.delete(user)
        session.commit()
        print("✅ Cleanup concluído")


def test_message_service():
    """Testa o Message Service"""
    print("\n" + "="*80)
    print("🧪 TESTE 3: Message Service")
    print("="*80)
    
    with Session(engine) as session:
        # Criar usuário e sessão temporários
        user = user_service.get_or_create_user(
            session,
            "5511977777777",
            "Pedro Teste"
        )
        user_session = session_service.get_or_create_open_session(session, user.id)
        
        # Salvar mensagens
        msg1 = message_service.save_message(
            session,
            user_session.id,
            "user",
            "Olá! Quero me cadastrar."
        )
        print(f"✅ Mensagem 1 salva: [{msg1.role}] {msg1.content}")
        
        msg2 = message_service.save_message(
            session,
            user_session.id,
            "model",
            "Olá! Claro, vou te ajudar. Qual é o seu nome completo?"
        )
        print(f"✅ Mensagem 2 salva: [{msg2.role}] {msg2.content}")
        
        msg3 = message_service.save_message(
            session,
            user_session.id,
            "user",
            "Pedro Silva"
        )
        print(f"✅ Mensagem 3 salva: [{msg3.role}] {msg3.content}")
        
        # Buscar mensagens recentes
        recent = message_service.get_recent_messages(session, user_session.id, limit=5)
        print(f"\n✅ Mensagens recentes ({len(recent)}):")
        for msg in recent:
            print(f"   [{msg.role}]: {msg.content[:50]}...")
        
        # Formatar para contexto
        formatted = message_service.format_messages_for_context(recent)
        print(f"\n✅ Contexto formatado:")
        print(formatted)
        
        # Cleanup
        for msg in [msg1, msg2, msg3]:
            session.delete(msg)
        session.delete(user_session)
        session.delete(user)
        session.commit()
        print("\n✅ Cleanup concluído")


def test_integration():
    """Testa integração entre todos os services"""
    print("\n" + "="*80)
    print("🧪 TESTE 4: Integração Completa")
    print("="*80)
    
    with Session(engine) as session:
        # Simular fluxo completo
        print("\n📱 Simulando usuário enviando mensagem...")
        
        # 1. Criar/buscar usuário
        user = user_service.get_or_create_user(
            session,
            "5511966666666",
            "Ana Completa"
        )
        print(f"1️⃣ Usuário: {user.name} (ID: {user.id})")
        
        # 2. Criar/buscar sessão
        user_session = session_service.get_or_create_open_session(session, user.id)
        print(f"2️⃣ Sessão: ID={user_session.id}, Status={user_session.status}")
        
        # 3. Salvar mensagem do usuário
        message_service.save_message(
            session,
            user_session.id,
            "user",
            "Oi! Meu nome é Ana e tenho 28 anos."
        )
        print(f"3️⃣ Mensagem do usuário salva")
        
        # 4. Calcular campos faltantes ANTES de atualizar
        missing_before = session_service.calculate_missing_fields(session, user_session)
        print(f"4️⃣ Campos faltantes ANTES: {len(missing_before)}")
        
        # 5. Atualizar form_data com dados extraídos
        session_service.update_form_data(
            session,
            user_session.id,
            {"nome": "Ana", "idade": 28}
        )
        print(f"5️⃣ Form data atualizado")
        
        # 6. Calcular campos faltantes DEPOIS
        user_session = session_service.get_session_by_id(session, user_session.id)
        missing_after = session_service.calculate_missing_fields(session, user_session)
        print(f"6️⃣ Campos faltantes DEPOIS: {len(missing_after)}")
        print(f"   Próximo campo a perguntar: {missing_after[0].key if missing_after else 'NENHUM'}")
        
        # 7. Salvar resposta da IA
        if missing_after:
            next_field = missing_after[0]
            message_service.save_message(
                session,
                user_session.id,
                "model",
                f"Ótimo! Agora, {next_field.description}"
            )
            print(f"7️⃣ Resposta da IA salva")
        
        # 8. Buscar histórico
        history = message_service.get_recent_messages(session, user_session.id)
        print(f"\n8️⃣ Histórico da conversa:")
        for msg in history:
            print(f"   [{msg.role}]: {msg.content[:60]}...")
        
        print("\n✅ FLUXO COMPLETO TESTADO COM SUCESSO!")
        
        # Cleanup
        for msg in message_service.get_all_messages(session, user_session.id):
            session.delete(msg)
        session.delete(user_session)
        session.delete(user)
        session.commit()
        print("✅ Cleanup concluído")


def run_all_tests():
    """Executa todos os testes"""
    print("="*80)
    print("🧪 TESTES DOS SERVICES - ZapForm")
    print("="*80)
    
    try:
        test_user_service()
        test_session_service()
        test_message_service()
        test_integration()
        
        print("\n" + "="*80)
        print("✅ TODOS OS TESTES DOS SERVICES PASSARAM!")
        print("="*80)
        print("\n📋 Próximos passos:")
        print("1. Fase 5: Integração com IA (Gemini)")
        print("2. Fase 6: Envio de mensagens WhatsApp")
        print("3. Fase 7: Orchestrator (juntar tudo)")
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ ERRO NOS TESTES: {e}")
        print("="*80)
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    run_all_tests()