# api_medica_lacre/Dockerfile
FROM python:3.11-slim

# Uso do formato ENV chave=valor (Padrão moderno)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock* /app/

# Configurar Poetry e instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiar o restante do código
COPY . /app/

EXPOSE 8000