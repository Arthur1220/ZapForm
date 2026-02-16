# 🤖 ZapForm - Sistema de Entrevista Automática via WhatsApp

Sistema inteligente que conduz entrevistas automatizadas via WhatsApp, coletando informações de forma dinâmica usando IA.

## 📋 Índice

- [Stack Tecnológica](#stack-tecnológica)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Desenvolvimento](#desenvolvimento)

## 🛠️ Stack Tecnológica

- **Python 3.11+**
- **FastAPI** - Framework web assíncrono
- **PostgreSQL 15** - Banco de dados relacional
- **SQLModel** - ORM (Pydantic + SQLAlchemy)
- **Docker & Docker Compose** - Containerização
- **WhatsApp Business API** - Mensageria (Meta Graph API v21.0)
- **Google Gemini** - Inteligência Artificial

## 🚀 Instalação

### Pré-requisitos

- Docker e Docker Compose instalados
- Conta Meta Business (para WhatsApp API)
- Google API Key (para Gemini)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone <seu-repositorio>
cd zapform
```

2. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

3. **Inicie os containers:**
```bash
docker-compose up -d
```

4. **Verifique se está rodando:**
```bash
curl http://localhost:8000/health
```

A API estará disponível em: `http://localhost:8000`
Documentação Swagger: `http://localhost:8000/docs`

## ⚙️ Configuração

### Variáveis de Ambiente

Edite o arquivo `.env` com suas credenciais:

```env
# Database
DATABASE_URL=postgresql://zapform_user:zapform_pass@db:5432/zapform_db

# WhatsApp Business API
WHATSAPP_API_TOKEN=seu_token_aqui
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id_aqui
WHATSAPP_VERIFY_TOKEN=seu_verify_token_aqui

# Google Gemini
GOOGLE_API_KEY=sua_api_key_aqui
```

### Obter Credenciais do WhatsApp

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Crie um App tipo "Business"
3. Adicione o produto "WhatsApp"
4. Configure um número de teste
5. Copie o `Phone Number ID` e o `Token`

### Obter API Key do Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova API Key
3. Copie e cole no `.env`

## 📖 Uso

### Configurar Webhook do WhatsApp

Para receber mensagens, configure o webhook no Meta:

1. No painel do Meta Developers, vá em WhatsApp > Configuration
2. Configure o webhook:
   - **URL:** `https://seu-dominio.com/webhook`
   - **Verify Token:** O mesmo definido em `WHATSAPP_VERIFY_TOKEN`
3. Inscreva-se no campo `messages`

### Testar Localmente com ngrok

```bash
# Instale o ngrok
brew install ngrok  # ou baixe de ngrok.com

# Exponha a porta 8000
ngrok http 8000

# Use a URL gerada no webhook do Meta
```

### Popular Dados Iniciais (Seed)

```bash
docker-compose exec api python seed.py
```

Isso criará perguntas padrão como: nome, idade, endereço, etc.

## 📁 Estrutura do Projeto

```
zapform/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configurações e variáveis de ambiente
│   │   └── database.py         # Setup do banco de dados
│   ├── models/                 # Modelos SQLModel (User, Session, etc)
│   │   └── __init__.py
│   ├── routers/                # Endpoints da API
│   │   └── __init__.py
│   └── services/               # Lógica de negócio
│       └── __init__.py
├── .env                        # Variáveis de ambiente (não commitar)
├── .env.example                # Template de variáveis
├── .gitignore
├── docker-compose.yml          # Orquestração dos containers
├── Dockerfile                  # Imagem da aplicação
├── requirements.txt            # Dependências Python
├── seed.py                     # Script para popular dados iniciais
└── README.md
```

## 🔌 API Endpoints

### Documentação Interativa

Acesse `/docs` para ver toda a documentação Swagger gerada automaticamente.

### Endpoints Principais

#### Health Check
```http
GET /health
```

#### Webhook WhatsApp
```http
GET /webhook?hub.mode=subscribe&hub.verify_token=TOKEN&hub.challenge=CHALLENGE
POST /webhook
```

#### Consultar Sessão
```http
GET /api/sessions/{phone_number}
```

## 🧪 Desenvolvimento

### Instalar Dependências Localmente

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Rodar Sem Docker

```bash
# Certifique-se que o PostgreSQL está rodando
export $(cat .env | xargs)
uvicorn app.main:app --reload
```

### Ver Logs

```bash
# Todos os containers
docker-compose logs -f

# Apenas API
docker-compose logs -f api

# Apenas Database
docker-compose logs -f db
```

### Acessar Container

```bash
# API
docker-compose exec api bash

# Database
docker-compose exec db psql -U zapform_user -d zapform_db
```

### Reiniciar Containers

```bash
docker-compose restart
```

### Parar Tudo

```bash
docker-compose down
```

### Limpar Volumes (cuidado!)

```bash
docker-compose down -v
```

## 🐛 Troubleshooting

### Erro: "Connection refused" no banco

```bash
# Verifique se o PostgreSQL está saudável
docker-compose ps

# Reinicie o container do banco
docker-compose restart db
```

### Erro: "Module not found"

```bash
# Reconstrua a imagem
docker-compose build --no-cache
docker-compose up -d
```

### Webhook não recebe mensagens

1. Verifique se o ngrok está rodando
2. Confirme que o URL no Meta está correto
3. Veja os logs: `docker-compose logs -f api`
4. Teste o webhook manualmente com curl

### Erro 401 na API do WhatsApp

- Verifique se o `WHATSAPP_API_TOKEN` está correto
- Tokens expiram - gere um novo token permanente

## 📝 Próximas Fases

- [ ] Fase 2: Modelos de dados (User, Session, Message, Infos)
- [ ] Fase 3: Webhook do WhatsApp
- [ ] Fase 4: Services de negócio
- [ ] Fase 5: Integração com Gemini
- [ ] Fase 6: Envio de mensagens WhatsApp
- [ ] Fase 7: API de gestão
- [ ] Fase 8: Segurança e tratamento de erros
- [ ] Fase 9: Deploy em produção

## 📄 Licença

Este projeto é privado e proprietário.

## 👥 Contribuindo

Para contribuir, siga o planejamento em `PLANEJAMENTO_ZAPFORM.md`.

---

**Desenvolvido com ❤️ usando FastAPI e SQLModel**