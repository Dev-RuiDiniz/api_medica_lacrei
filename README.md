# 🏥 API Lacrei Saúde - Gestão Médica

API robusta para gestão de profissionais de saúde e agendamento de consultas, desenvolvida com Django Rest Framework, Docker e PostgreSQL. 

## 🚀 Tecnologias Utilizadas
* **Python 3.11**
* **Django 5.2 & DRF** (Framework Web e API)
* **PostgreSQL** (Banco de dados relacional)
* **Poetry** (Gestão de dependências)
* **Docker & Docker Compose** (Containerização)

---

## 🗂️ Estrutura do Projeto e Arquivos Importantes

```
api_medica_lacrei/
│
├── core/               # Configurações globais Django (settings, urls, wsgi etc)
├── users/              # App principal: modelos, views, serializers, regras e testes
│   ├── migrations/     # Migrações do banco
│   └── tests/          # Testes unitários e integrados
│
├── Dockerfile          # Para build do container web Python/Django
├── docker-compose.yml  # Orquestração dos serviços web/db
├── pyproject.toml      # Dependências (Poetry)
├── requirements.txt    # Dependências (pip freeze)
├── main.tf             # Configuração Infraestrutura (Terraform - deploy AWS)
├── README.md           # Documentação principal
├── manage.py           # CLI Django
└── ...
```

### Principais Funcionalidades e Arquivos:
- **App `users`**: Gestão de profissionais, consultas, regras de negócio e serviços externos (pagamento).
- **Camada de testes completa**: `users/tests/` cobre autenticação, segurança, business rules, views e integração.
- **Bleach**: Sanitização de texto nos serializers (prevenção XSS).
- **Integração com gateway Asaas**: Cobranças automáticas mockadas em testes.
- **Infraestrutura pronta para produção**: Docker (web/db), variáveis de ambiente, scripts migration/admin e deploy cloud (`main.tf`).

### Dependências Principais
- Django, DRF, djangorestframework-simplejwt (JWT)
- PostgreSQL, psycopg2-binary
- bleach, django-cors-headers, django-filter
- Pytest, coverage, flake8 (qualidade)

### Observações
- O deploy cloud utiliza `main.tf` com AWS AppRunner; ambiente dockerizado ready-to-go.
- Os dados sensíveis (senhas, keys) ficam no `.env`, não versionado.

---

## 🛠️ Configuração e Instalação (Docker)

### Pré-requisitos
* Docker e Docker Compose instalados.

### Passos
1. **Clonar o repositório:**
   
   ```bash
   git clone [https://github.com/Dev-RuiDiniz/api_medica_lacrei.git](https://github.com/Dev-RuiDiniz/api_medica_lacrei.git)
   cd api_medica_lacrei
   ```

2. Configurar variáveis de ambiente: Crie um arquivo .env na raiz com base no exemplo:

    ```Snippet de código

    SECRET_KEY=sua_chave_secreta
    DEBUG=True
    DB_NAME=lacre_db
    DB_USER=lacre_user
    DB_PASS=lacre_pass
    DB_HOST=db
    DB_PORT=5432
    ```

3. Subir os containers:

    ```bash

    docker-compose up -d --build
    ```

4. Executar migrações iniciais:

    ```bash

    docker-compose exec web python manage.py migrate
    ```

5. Criar usuário administrador:

    ```bash

    docker-compose exec web python manage.py createsuperuser
    Acesse o painel administrativo em: http://localhost:8000/admin
    ```

## 📦 Gestão de Dependências (Local)

Caso queira rodar comandos do Poetry localmente:

    ```bash

    poetry install
    poetry shell
    ```

## 📐 Arquitetura do Projeto

O projeto segue os princípios Twelve-Factor App, garantindo que a configuração seja separada do código e que o ambiente de desenvolvimento seja idêntico ao de produção.

## 🛡️ Decisões Técnicas e Segurança

Nesta fase do projeto, implementamos camadas de segurança seguindo as melhores práticas da OWASP e do ecossistema Django.

### 1. Autenticação via JWT (JSON Web Token)
Optamos pelo padrão **JWT (SimpleJWT)** em vez da autenticação por sessão padrão do Django pelos seguintes motivos:
- **Stateless**: O servidor não precisa armazenar sessões em memória, facilitando a escalabilidade em containers.
- **Interoperabilidade**: Facilita a integração com aplicações Mobile e Frontends modernos (React/Vue/Mobile).
- **Segurança**: Tokens possuem tempo de expiração curto (60 minutos) e necessidade de Refresh Token, minimizando danos em caso de vazamento.

### 2. Sanitização de Dados (Prevenção contra XSS)
Para garantir a integridade dos dados e proteger os usuários que visualizarão as informações (como nomes de profissionais e pacientes), implementamos a biblioteca **Bleach** nos serializers:
- **Filtro Ativo**: Todos os campos de texto são limpos antes de chegarem ao banco de dados PostgreSQL.
- **Remoção de Tags**: Scripts maliciosos como `<script>` ou tags HTML indesejadas são removidos automaticamente, prevenindo ataques de *Stored Cross-Site Scripting*.

### 3. Regras de Negócio e Integridade
As validações foram implementadas em duas camadas:
- **Serializers**: Para fornecer respostas rápidas e amigáveis ao usuário via API.
- **Models (clean/save)**: Como uma "última linha de defesa" para garantir que, mesmo via Django Admin ou Scripts, não existam consultas em datas passadas ou conflitos de horário para o mesmo profissional.

### 4. Observabilidade (Logs)
Configuramos um sistema de logging estruturado que diferencia logs de erro (salvos em arquivo) e logs de operação (auditoria de quem criou/editou registros), essencial para conformidade em sistemas de saúde.

## 💰 Integração com Gateway de Pagamento (Bônus)

Implementamos uma arquitetura de serviços para integração com o **Asaas**, permitindo a cobrança automática via PIX no momento do agendamento.

### Fluxo de Pagamento:
1. **Trigger**: Ao salvar uma nova `Consulta`, o `AsaasService` é invocado.
2. **Customer Creation**: O sistema verifica/cria o cliente no gateway.
3. **Payment Generation**: É gerada uma cobrança com `externalReference` vinculado ao ID da consulta para conciliação bancária via Webhook.

*Nota: Atualmente operando em modo Mock para preservação de credenciais de Sandbox.*

## 🧪 Testes e Qualidade de Código

Esta API foi desenvolvida seguindo rigorosos padrões de qualidade, com foco em segurança, integridade de dados e cobertura de testes.

### 📊 Métricas de Cobertura
Atualmente, o projeto conta com **93% de cobertura de código**, garantindo que as principais regras de negócio e fluxos de segurança estejam protegidos contra regressões.

### 🛠️ Como rodar a suíte de testes

Certifique-se de que os containers do Docker estejam rodando (`docker-compose up -d`).

1. Executar todos os testes (Pytest)

Para rodar os 24 testes unitários e de integração:

```bash

docker-compose exec web pytest
```

2. Gerar Relatório de Cobertura (Coverage)

Para visualizar a cobertura de testes no terminal:

```bash

docker-compose exec web pytest --cov=users
```

Para gerar o relatório detalhado em HTML (abrir a pasta htmlcov/index.html após o comando):

```bash

docker-compose exec web pytest --cov=users --cov-report=html
```

3. Verificação de Estilo e Lint (PEP8)
Garantimos que o código segue as normas da PEP8 utilizando o flake8:

```bash

docker-compose exec web flake8 .
```

### 🔍 O que está sendo testado?

- Autenticação: Bloqueio de acesso a usuários sem Token JWT ou com tokens inválidos.
- Segurança (XSS): Validação da limpeza de campos de texto (sanitização) contra injeção de scripts.
- Regras de Negócio:
- Impedimento de agendamentos em datas retroativas.
- Bloqueio de conflitos de horário (um profissional não pode ter duas consultas no mesmo horário).
- CRUD Completo: Validação de criação, leitura, edição parcial (PATCH) e deleção de Profissionais e Consultas.
- Integração Bônus: Simulação do fluxo de pagamento via API do Asaas.

## Desenvolvido por Rui Diniz - Dezembro 2025.