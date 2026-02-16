"""
Script para verificar a conexão com o banco de dados.
Execute: docker-compose exec api python verify_database.py
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models import User, Info, Session as SessionModel, Message


def verify_database_connection():
    """Verifica se a conexão com o banco está funcionando"""
    print("=" * 80)
    print("🔍 VERIFICAÇÃO DA CONEXÃO COM O BANCO DE DADOS")
    print("=" * 80)
    
    try:
        # Teste 1: Criar uma conexão
        print("\n📊 Teste 1: Criando conexão com o banco...")
        with Session(engine) as session:
            print("✅ Conexão estabelecida com sucesso!")
            
            # Teste 2: Executar uma query simples
            print("\n📊 Teste 2: Executando query de teste...")
            result = session.exec(select(1)).first()
            print(f"✅ Query executada! Resultado: {result}")
            
            # Teste 3: Verificar se as tabelas existem
            print("\n📊 Teste 3: Verificando tabelas...")
            
            # Verificar tabela users
            users_count = session.exec(select(User)).all()
            print(f"✅ Tabela 'users' existe e tem {len(users_count)} registros")
            
            # Verificar tabela infos
            infos_count = session.exec(select(Info)).all()
            print(f"✅ Tabela 'infos' existe e tem {len(infos_count)} registros")
            
            # Verificar tabela sessions
            sessions_count = session.exec(select(SessionModel)).all()
            print(f"✅ Tabela 'sessions' existe e tem {len(sessions_count)} registros")
            
            # Verificar tabela messages
            messages_count = session.exec(select(Message)).all()
            print(f"✅ Tabela 'messages' existe e tem {len(messages_count)} registros")
            
            # Teste 4: Criar e deletar um registro de teste
            print("\n📊 Teste 4: Criando registro de teste...")
            test_user = User(
                phone_number="5511000000000",
                name="Teste Conexão"
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            print(f"✅ User de teste criado com ID: {test_user.id}")
            
            # Deletar o registro de teste
            session.delete(test_user)
            session.commit()
            print("✅ User de teste deletado com sucesso!")
            
            print("\n" + "=" * 80)
            print("✅ TODOS OS TESTES DE CONEXÃO PASSARAM!")
            print("=" * 80)
            
            print("\n📋 Resumo:")
            print(f"   - Conexão: ✅ Funcionando")
            print(f"   - Tabelas: ✅ Todas criadas")
            print(f"   - Users: {len(users_count)} registros")
            print(f"   - Infos: {len(infos_count)} registros (execute seed.py se estiver 0)")
            print(f"   - Sessions: {len(sessions_count)} registros")
            print(f"   - Messages: {len(messages_count)} registros")
            print(f"   - CRUD: ✅ Funcionando")
            
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ ERRO NA CONEXÃO COM O BANCO!")
        print("=" * 80)
        print(f"\nErro: {e}")
        print("\nPossíveis causas:")
        print("1. Container do banco não está rodando")
        print("2. Credenciais incorretas no .env")
        print("3. Tabelas não foram criadas")
        print("\nComandos para debug:")
        print("  docker-compose ps")
        print("  docker-compose logs db")
        print("  docker-compose logs api")
        raise


if __name__ == "__main__":
    verify_database_connection()