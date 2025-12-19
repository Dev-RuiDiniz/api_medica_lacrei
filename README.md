# 🏥 API Lacrei Saúde - Gestão Médica

API robusta para gestão de profissionais de saúde e agendamento de consultas, desenvolvida com Django Rest Framework, Docker e PostgreSQL. 

## 🚀 Tecnologias Utilizadas
* **Python 3.11**
* **Django 5.2 & DRF** (Framework Web e API)
* **PostgreSQL** (Banco de dados relacional)
* **Poetry** (Gestão de dependências)
* **Docker & Docker Compose** (Containerização)

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

    ```Bash

    docker-compose up -d --build
    ```

4. Executar migrações iniciais:

    ```Bash

    docker-compose exec web python manage.py migrate
    ```

5. Criar usuário administrador:

    ```Bash

    docker-compose exec web python manage.py createsuperuser
    Acesse o painel administrativo em: http://localhost:8000/admin
    ```

## 📦 Gestão de Dependências (Local)
Caso queira rodar comandos do Poetry localmente:

    ```Bash

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

## Desenvolvido por Rui Diniz - Dezembro 2025.