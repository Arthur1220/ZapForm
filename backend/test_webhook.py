"""
Script de teste para o webhook do WhatsApp.
Simula requisições do Meta para testar o endpoint.
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_webhook_verification():
    """Testa a verificação do webhook (GET)"""
    print("\n" + "="*80)
    print("🧪 TESTE 1: Verificação do Webhook (GET)")
    print("="*80)
    
    # Parâmetros que o Meta envia
    params = {
        "hub.mode": "subscribe",
        "hub.challenge": "123456789",
        "hub.verify_token": "seu_token_de_verificacao_webhook"  # Deve ser igual ao .env
    }
    
    print(f"\n📤 Enviando GET para {BASE_URL}/webhook")
    print(f"   Parâmetros: {params}")
    
    try:
        response = requests.get(f"{BASE_URL}/webhook", params=params)
        
        print(f"\n📥 Resposta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            print("\n✅ SUCESSO! Webhook verificado corretamente")
            print(f"   Challenge retornado: {response.text}")
        else:
            print(f"\n❌ ERRO! Status: {response.status_code}")
            print(f"   Verifique se o WHATSAPP_VERIFY_TOKEN no .env está correto")
            
    except Exception as e:
        print(f"\n❌ ERRO na requisição: {e}")


def test_webhook_text_message():
    """Testa recebimento de mensagem de texto (POST)"""
    print("\n" + "="*80)
    print("🧪 TESTE 2: Recebimento de Mensagem de Texto (POST)")
    print("="*80)
    
    # Payload que o Meta envia quando usuário manda mensagem
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "5511999999999",
                                "phone_number_id": "123456789"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": "João Silva Teste"
                                    },
                                    "wa_id": "5511988888888"
                                }
                            ],
                            "messages": [
                                {
                                    "from": "5511988888888",
                                    "id": "wamid.test123",
                                    "timestamp": "1234567890",
                                    "text": {
                                        "body": "Olá! Quero fazer o cadastro."
                                    },
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    print(f"\n📤 Enviando POST para {BASE_URL}/webhook")
    print(f"   Payload simulado do Meta:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📥 Resposta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Body: {response.json()}")
        
        if response.status_code == 200:
            print("\n✅ SUCESSO! Mensagem recebida e processada")
        else:
            print(f"\n❌ ERRO! Status: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ ERRO na requisição: {e}")


def test_webhook_audio_message():
    """Testa recebimento de mensagem de áudio (POST)"""
    print("\n" + "="*80)
    print("🧪 TESTE 3: Recebimento de Mensagem de Áudio (POST)")
    print("="*80)
    
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "5511999999999",
                                "phone_number_id": "123456789"
                            },
                            "contacts": [
                                {
                                    "profile": {
                                        "name": "Maria Santos Teste"
                                    },
                                    "wa_id": "5511977777777"
                                }
                            ],
                            "messages": [
                                {
                                    "from": "5511977777777",
                                    "id": "wamid.audio123",
                                    "timestamp": "1234567890",
                                    "audio": {
                                        "id": "audio_file_id_123",
                                        "mime_type": "audio/ogg; codecs=opus"
                                    },
                                    "type": "audio"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    print(f"\n📤 Enviando POST para {BASE_URL}/webhook")
    print(f"   Simulando mensagem de áudio...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📥 Resposta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Body: {response.json()}")
        
        if response.status_code == 200:
            print("\n✅ SUCESSO! Áudio recebido (tratado como [ÁUDIO])")
        else:
            print(f"\n❌ ERRO! Status: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ ERRO na requisição: {e}")


def test_webhook_status_update():
    """Testa recebimento de status update (deve ser ignorado)"""
    print("\n" + "="*80)
    print("🧪 TESTE 4: Status Update - Deve ser Ignorado (POST)")
    print("="*80)
    
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "123456789",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "5511999999999",
                                "phone_number_id": "123456789"
                            },
                            "statuses": [
                                {
                                    "id": "wamid.status123",
                                    "status": "delivered",
                                    "timestamp": "1234567890",
                                    "recipient_id": "5511988888888"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }
    
    print(f"\n📤 Enviando POST para {BASE_URL}/webhook")
    print(f"   Simulando status update (delivered)...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📥 Resposta:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Body: {response.json()}")
        
        if response.status_code == 200:
            print("\n✅ SUCESSO! Status update ignorado corretamente")
        else:
            print(f"\n❌ ERRO! Status: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ ERRO na requisição: {e}")


def run_all_tests():
    """Executa todos os testes"""
    print("="*80)
    print("🧪 TESTES DO WEBHOOK - ZapForm")
    print("="*80)
    print("\nCertifique-se de que:")
    print("1. O docker-compose está rodando (docker-compose up -d)")
    print("2. A API está acessível em http://localhost:8000")
    print("3. O WHATSAPP_VERIFY_TOKEN no .env está configurado")
    
    input("\nPressione ENTER para iniciar os testes...")
    
    try:
        test_webhook_verification()
        test_webhook_text_message()
        test_webhook_audio_message()
        test_webhook_status_update()
        
        print("\n" + "="*80)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("="*80)
        print("\n📋 Próximos passos:")
        print("1. Verifique os logs: docker-compose logs -f api")
        print("2. Acesse a documentação: http://localhost:8000/docs")
        print("3. Configure o webhook no Meta com sua URL pública (ngrok)")
        
    except Exception as e:
        print("\n" + "="*80)
        print(f"❌ ERRO NOS TESTES: {e}")
        print("="*80)


if __name__ == "__main__":
    run_all_tests()