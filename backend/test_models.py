"""
Script de teste para validar os modelos e banco de dados.
Execute: docker-compose exec api python test_models.py
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.user import User
from app.models.info import Info
from app.models.session import Session as SessionModel
from app.models.message import Message


def test_user_crud():
    """Testa operações CRUD no modelo User"""
    print("\n🧪 Testando modelo User...")
    
    with Session(engine) as session:
        # CREATE
        user = User(
            phone_number="5511999999999",
            name="João Teste"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"✅ User criado: ID={user.id}, Nome={user.name}")
        
        # READ
        db_user = session.exec(
            select(User).where(User.phone_number == "5511999999999")
        ).first()
        print(f"✅ User lido: {db_user.name}")
        
        # UPDATE
        db_user.name = "João Silva Atualizado"
        session.add(db_user)
        session.commit()
        print(f"✅ User atualizado: {db_user.name}")
        
        # DELETE
        session.delete(db_user)
        session.commit()
        print("✅ User deletado")


def test_info_query():
    """Testa consulta de Infos"""
    print("\n🧪 Testando modelo Info...")
    
    with Session(engine) as session:
        infos = session.exec(select(Info).order_by(Info.order)).all()
        
        if not infos:
            print("⚠️  Nenhum Info encontrado. Execute o seed primeiro!")
            return
        
        print(f"✅ Total de Infos: {len(infos)}")
        for info in infos:
            print(f"   - {info.key} (ordem {info.order})")


def test_session_with_json():
    """Testa Session com campo JSONB"""
    print("\n🧪 Testando modelo Session com JSONB...")
    
    with Session(engine) as session:
        # Criar um usuário temporário
        user = User(phone_number="5511988888888", name="Maria Teste")
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Criar sessão com form_data
        session_model = SessionModel(
            user_id=user.id,
            status="OPEN",
            form_data={
                "nome": "Maria",
                "idade": 25,
                "cidade": "São Paulo"
            }
        )
        session.add(session_model)
        session.commit()
        session.refresh(session_model)
        
        print(f"✅ Session criada: ID={session_model.id}")
        print(f"   Status: {session_model.status}")
        print(f"   Form Data: {session_model.form_data}")
        
        # Atualizar form_data
        session_model.form_data["email"] = "maria@example.com"
        session.add(session_model)
        session.commit()
        
        print(f"✅ Form Data atualizado: {session_model.form_data}")
        
        # Cleanup
        session.delete(session_model)
        session.delete(user)
        session.commit()
        print("✅ Cleanup concluído")


def test_message_creation():
    """Testa criação de mensagens"""
    print("\n🧪 Testando modelo Message...")
    
    with Session(engine) as session:
        # Criar usuário e sessão temporários
        user = User(phone_number="5511977777777", name="Pedro Teste")
        session.add(user)
        session.commit()
        session.refresh(user)
        
        session_model = SessionModel(
            user_id=user.id,
            status="OPEN",
            form_data={}
        )
        session.add(session_model)
        session.commit()
        session.refresh(session_model)
        
        # Criar mensagens
        msg1 = Message(
            session_id=session_model.id,
            role="user",
            content="Olá!"
        )
        msg2 = Message(
            session_id=session_model.id,
            role="model",
            content="Olá! Como posso ajudar?"
        )
        
        session.add(msg1)
        session.add(msg2)
        session.commit()
        
        print(f"✅ Mensagens criadas")
        
        # Buscar mensagens da sessão
        messages = session.exec(
            select(Message)
            .where(Message.session_id == session_model.id)
            .order_by(Message.timestamp)
        ).all()
        
        print(f"✅ Total de mensagens: {len(messages)}")
        for msg in messages:
            print(f"   [{msg.role}]: {msg.content}")
        
        # Cleanup
        for msg in messages:
            session.delete(msg)
        session.delete(session_model)
        session.delete(user)
        session.commit()
        print("✅ Cleanup concluído")


def test_missing_fields_calculation():
    """Simula cálculo de campos faltantes"""
    print("\n🧪 Testando cálculo de campos faltantes...")
    
    with Session(engine) as session:
        # Buscar todos os infos
        all_infos = session.exec(select(Info).order_by(Info.order)).all()
        
        if not all_infos:
            print("⚠️  Execute o seed primeiro!")
            return
        
        # Simular form_data parcialmente preenchido
        form_data = {
            "nome": "Carlos",
            "idade": 30
        }
        
        # Calcular campos faltantes
        required_keys = {info.key for info in all_infos}
        filled_keys = set(form_data.keys())
        missing_keys = required_keys - filled_keys
        
        print(f"✅ Total de campos obrigatórios: {len(required_keys)}")
        print(f"✅ Campos preenchidos: {len(filled_keys)} - {filled_keys}")
        print(f"✅ Campos faltantes: {len(missing_keys)} - {missing_keys}")
        
        # Buscar os Infos faltantes
        missing_infos = [info for info in all_infos if info.key in missing_keys]
        
        print(f"\n📋 Próximas perguntas a fazer:")
        for info in missing_infos[:3]:  # Mostrar apenas as 3 primeiras
            print(f"   - {info.key}: {info.description[:60]}...")


def run_all_tests():
    """Executa todos os testes"""
    print("=" * 80)
    print("🧪 TESTES DOS MODELOS - ZapForm")
    print("=" * 80)
    
    try:
        test_user_crud()
        test_info_query()
        test_session_with_json()
        test_message_creation()
        test_missing_fields_calculation()
        
        print("\n" + "=" * 80)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 80)
        
    except Exception as e:
        print("\n" + "=" * 80)
        print(f"❌ ERRO NOS TESTES: {e}")
        print("=" * 80)
        raise


if __name__ == "__main__":
    run_all_tests()