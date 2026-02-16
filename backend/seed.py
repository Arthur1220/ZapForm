"""
Script de seed para popular a tabela Infos com dados iniciais.
Execute: docker-compose exec api python seed.py
"""
from sqlmodel import Session, select
from app.core.database import engine
from app.models.info import Info


def seed_infos():
    """
    Popula a tabela Infos com campos padrão do formulário.
    """
    print("🌱 Iniciando seed da tabela Infos...")
    
    # Dados iniciais do formulário
    infos_data = [
        {
            "key": "nome",
            "description": "Pergunte o nome completo do usuário. Seja educado e amigável.",
            "order": 1
        },
        {
            "key": "idade",
            "description": "Pergunte a idade do usuário. Deve ser um número inteiro. Valide se é maior que 18 anos.",
            "order": 2
        },
        {
            "key": "email",
            "description": "Pergunte o email do usuário. Valide se está em formato válido (contém @ e domínio).",
            "order": 3
        },
        {
            "key": "cidade",
            "description": "Pergunte em qual cidade o usuário mora. Inclua o estado se possível.",
            "order": 4
        },
        {
            "key": "profissao",
            "description": "Pergunte qual é a profissão ou área de atuação do usuário.",
            "order": 5
        },
        {
            "key": "interesse",
            "description": "Pergunte qual é o principal interesse ou motivo do contato. Seja específico.",
            "order": 6
        }
    ]
    
    with Session(engine) as session:
        # Verificar se já existem dados
        existing_count = len(session.exec(select(Info)).all())
        
        if existing_count > 0:
            print(f"⚠️  Tabela Infos já contém {existing_count} registros.")
            print("🔄 Deseja recriar? (Isso irá deletar os dados existentes)")
            response = input("Digite 'sim' para confirmar: ")
            
            if response.lower() != 'sim':
                print("❌ Operação cancelada.")
                return
            
            # Deletar registros existentes
            print("🗑️  Deletando registros existentes...")
            for info in session.exec(select(Info)).all():
                session.delete(info)
            session.commit()
        
        # Inserir novos dados
        print(f"📝 Inserindo {len(infos_data)} campos no formulário...")
        
        for data in infos_data:
            info = Info(**data)
            session.add(info)
        
        session.commit()
        print("✅ Seed concluído com sucesso!")
        
        # Mostrar resumo
        print("\n📋 Campos criados:")
        for info in session.exec(select(Info).order_by(Info.order)).all():
            print(f"  {info.order}. {info.key}: {info.description[:60]}...")


def verify_infos():
    """
    Verifica e exibe os dados da tabela Infos.
    """
    print("\n🔍 Verificando dados na tabela Infos...")
    
    with Session(engine) as session:
        infos = session.exec(select(Info).order_by(Info.order)).all()
        
        if not infos:
            print("❌ Nenhum dado encontrado. Execute o seed primeiro!")
            return
        
        print(f"\n✅ Total de campos cadastrados: {len(infos)}\n")
        print("=" * 80)
        
        for info in infos:
            print(f"ID: {info.id} | Ordem: {info.order}")
            print(f"Key: {info.key}")
            print(f"Descrição: {info.description}")
            print(f"Criado em: {info.created_at}")
            print("-" * 80)


if __name__ == "__main__":
    import sys
    
    print("=" * 80)
    print("🌱 SEED SCRIPT - ZapForm")
    print("=" * 80)
    
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        verify_infos()
    else:
        seed_infos()
        verify_infos()
    
    print("\n✨ Operação concluída!")