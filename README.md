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


## Desenvolvido por Rui Diniz - Dezembro 2025.