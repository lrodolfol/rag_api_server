
# rag_api_server

## Descrição
O `rag_api_server` é uma API desenvolvida em Python utilizando Flask, com foco em servir como backend para aplicações de perguntas e respostas (RAG - Retrieval Augmented Generation), integrando serviços de IA, armazenamento de históricos de chat, autenticação de usuários, limitação de requisições e persistência de dados em banco relacional (PostgreSQL) e Redis.

## Funcionalidades Principais
- **Autenticação JWT**: Geração e validação de tokens para acesso seguro às rotas.
- **Limitação de Requisições**: Uso do Flask-Limiter com Redis para controle de rate limit.
- **Integração com IA**: Comunicação com serviços de IA (OpenAI, Pinecone, LangChain) para respostas automáticas e enriquecidas.
- **Gerenciamento de Usuários**: Cadastro, autenticação e controle de acesso de usuários e cartões de crédito.
- **Histórico de Conversas**: Armazenamento e recuperação de históricos de chat.
- **Agendamento de Tarefas**: Uso do APScheduler para tarefas automáticas (ex: expiração de usuários).
- **Gerenciamento de Arquivos**: Upload, leitura e manipulação de arquivos de clientes e serviços.

## Estrutura de Pastas
- `app.py`: Arquivo principal da aplicação Flask.
- `api_manager/`: Gerencia respostas customizadas da API.
- `configuration/`: Configurações para diferentes ambientes (dev/prod).
- `dao/`: Objetos de acesso a dados (ex: usuários, cartões).
- `files_source/`: Fontes de dados, históricos e arquivos de clientes.
- `gateways/`: Integrações externas (OpenAI, Pinecone, Redis, Email, HTTP, etc).
- `handlers/`: Lógica de negócio das rotas (ex: autenticação, perguntas, arquivos).
- `models/`: Modelos de dados e entidades.
- `queries/`: Scripts SQL e dumps.
- `routes/`: Definição das rotas da API.
- `static/`: Utilitários, configurações e serviços auxiliares.


## Instalação e Uso Rápido
1. Clone o repositório:
	```bash
	git clone <repo_url>
	cd rag_api_server
	```
2. Crie o ambiente virtual e instale as dependências:
	```bash
	make install
	```
3. Configure as variáveis de ambiente necessárias (exemplo abaixo).
4. Execute a aplicação:
	```bash
	make run
	```

## Comandos Úteis (Makefile)
- `make install` — Cria o ambiente virtual e instala dependências
- `make run` — Executa a aplicação
- `make lint` — Analisa o código com flake8
- `make format` — Formata o código com black
- `make clean` — Remove arquivos temporários e o venv

## Endpoints Principais
- `POST /api/v1/askme`: Envia perguntas para o sistema de IA.
- `POST /api/v1/auth`: Autenticação e geração de token JWT.
- `GET /api/v1/home`: Teste de funcionamento da API.

## Dependências Principais
- Flask, Flask-Limiter, flask-cors
- APScheduler
- psycopg2
- Redis
- OpenAI, Pinecone, LangChain

## Boas Práticas e Observações
- Utilize sempre o ambiente virtual (`venv`) para evitar conflitos de dependências.
- O projeto utiliza banco de dados PostgreSQL (banco padrão: tinosnegocios) e Redis. Certifique-se de que ambos estejam configurados e acessíveis.
- Para integração com IA, configure as chaves de API necessárias nos ambientes.
- Para produção, utilize um servidor WSGI como Gunicorn.

---