# FilmesTop API

API para gestão de filmes, construída com Flask e PostgreSQL.

---

## Como rodar o projeto

### 1. Crie um arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
# Configurações do banco de dados
POSTGRES_USER=filmes_top
POSTGRES_PASSWORD=base
POSTGRES_DB=filmes_top
PG_PORT=5432
PG_HOST=database

DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${PG_HOST}:${PG_PORT}/${POSTGRES_DB}

# Configurações do Flask
FLASK_ENV=production
FLASK_APP=main.py
JWT_SECRET_KEY=your_jwt_secret_key
```

### 2. Suba o ambiente com Docker

```bash
docker compose up --build
```

A API estará disponível em: http://localhost:5000

## Documentação da API

Acesse a documentação completa dos endpoints em:

👉 http://localhost:5000/apidocs
