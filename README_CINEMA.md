# Cinema Review — Sistema de Avaliação de Filmes

Uma aplicação full-stack (Frontend + Backend) para gerenciar um catálogo de filmes e avaliações, inspirada em plataformas como Letterboxd.

## Stack Tecnológico

- **Frontend:** Vite + React 18.2 + TypeScript
- **Backend:** FastAPI (Python 3.11+)
- **Banco de Dados:** SQLite com Alembic (migrations)
- **Padrão de Dados:** Esquema estrela (star schema)

## Funcionalidades

### ✅ Implementadas

- **Catálogo Paginado:** Listar todos os filmes com paginação (10 por página)
- **Busca:** Pesquisar filmes por título em tempo real
- **Detalhes do Filme:** Visualizar informações completas (sinopse, diretor, gênero, duração, poster)
- **Avaliações:** Ver histórico de avaliações com notas e comentários
- **Média de Avaliações:** Cálculo automático da nota média (escala 0-10, exibida em estrelas)
- **CRUD Completo:**
  - ✅ **Criar:** Novo filme com gênero/diretor (get-or-create automático)
  - ✅ **Ler:** Listar e detalhar filmes
  - ✅ **Atualizar:** Editar informações do filme
  - ✅ **Deletar:** Remover filme (com confirmação)
- **Adicionar Avaliação:** Nome, nota (0-10) e comentário
- **Limpeza de Dados:** Remoção automática de caracteres corrompidos de títulos
- **Interface Responsiva:** Funciona em desktop, tablet e mobile
- **Dark Mode:** Suporte a tema escuro via CSS

## Requisitos

- **Python 3.11+**
- **Node.js 16+** (para o frontend)
- **npm** (gerenciador de pacotes Node)

## Instalação e Execução

### 1. Backend

```bash
cd backend

# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate

# Instalar dependências
pip install -e ".[dev]"

# Configurar variáveis de ambiente
cp .env.example .env

# Criar schema do banco
alembic upgrade head

# Opcional: Popular o banco com dados dos CSVs
# (Se os CSVs estiverem em /home/lucas/DESAFIO/cinema/bases-1/ e bases-2/)
python scripts/seed.py

# Iniciar o servidor
uvicorn app.main:app --reload
```

O backend estará disponível em: **http://localhost:8000**

- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

### 2. Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: **http://localhost:5173**

## Endpoints da API

### Filmes

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/v1/movies?page=1&page_size=10&search=titulo` | Listar filmes (paginado, com busca opcional) |
| `GET` | `/api/v1/movies/{id}` | Detalhes do filme (id = sk_movie_id ou id_filme) |
| `POST` | `/api/v1/movies` | Criar novo filme |
| `PUT` | `/api/v1/movies/{id}` | Atualizar filme |
| `DELETE` | `/api/v1/movies/{id}` | Deletar filme |

### Avaliações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `POST` | `/api/v1/movies/{id}/reviews` | Adicionar avaliação a um filme |

## Estrutura do Projeto

```
.
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   └── router.py          # Composição dos routers
│   │   ├── core/
│   │   │   ├── config.py          # Configurações
│   │   │   └── logging.py         # Logging
│   │   ├── db/
│   │   │   ├── base.py            # Base do SQLAlchemy
│   │   │   └── session.py         # AsyncSession factory
│   │   ├── movies/
│   │   │   ├── models.py          # ORM SQLAlchemy
│   │   │   ├── schemas.py         # Pydantic (request/response)
│   │   │   ├── repository.py      # Acesso a dados
│   │   │   ├── service.py         # Regras de negócio
│   │   │   └── router.py          # Endpoints FastAPI
│   │   └── main.py                # App principal
│   ├── migrations/                # Alembic migrations
│   ├── scripts/
│   │   └── seed.py                # Carrega dados dos CSVs
│   ├── tests/
│   │   ├── conftest.py            # Configuração pytest
│   │   └── test_movies.py         # Testes dos endpoints (39 testes)
│   └── pyproject.toml             # Dependências e config
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── types.ts           # TypeScript interfaces
│   │   │   ├── client.ts          # HTTP client
│   │   │   └── movies.ts          # Funções de API
│   │   ├── components/            # Componentes reutilizáveis
│   │   │   ├── MovieCard.tsx
│   │   │   ├── SearchBar.tsx
│   │   │   ├── Pagination.tsx
│   │   │   ├── StarRating.tsx
│   │   │   ├── ReviewList.tsx
│   │   │   ├── ReviewForm.tsx
│   │   │   ├── MovieForm.tsx
│   │   │   └── ConfirmDialog.tsx
│   │   ├── pages/                 # Páginas
│   │   │   ├── CatalogPage.tsx
│   │   │   ├── MovieDetailPage.tsx
│   │   │   └── MovieFormPage.tsx
│   │   ├── styles/
│   │   │   └── index.css          # Stylesheet global
│   │   ├── App.tsx                # Componente wrapper
│   │   ├── router.tsx             # Configuração React Router
│   │   └── main.tsx               # Entry point
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── index.html
│
└── README_CINEMA.md               # Este arquivo
```

## Fluxo de Dados

```
Frontend (React)
    ↓
API HTTP (fetch/axios)
    ↓
Backend (FastAPI)
    ├── Router (validação de request)
    ├── Service (regras de negócio)
    ├── Repository (acesso a dados)
    └── Database (SQLite)
```

## Características Técnicas

### Backend

- **Async/Await:** Operações de banco assíncronas
- **SQLAlchemy 2.0:** ORM moderno com type hints
- **Pydantic v2:** Validação e serialização de dados com field validators
- **Alembic:** Versionamento de schema
- **Logging:** Rastreamento de operações
- **Limpeza de Dados:** Remoção automática de caracteres corrompidos
- **Soft Search:** Busca case-insensitive com ilike
- **Cascade Delete:** Deletar filme remove reviews automaticamente
- **Get-or-Create Pattern:** Deduplica gêneros e diretores

### Frontend

- **Vite:** Build tool rápido
- **React Router v6:** Roteamento client-side
- **TypeScript:** Type safety
- **Componentes Funcionais:** Com React Hooks
- **Validação de Formulários:** Client-side
- **Tratamento de Erros:** User-friendly
- **CSS Responsivo:** Mobile-first design
- **Dark Mode:** Support nativo com CSS variables

## Testes

```bash
cd backend

# Rodar testes
pytest

# Com cobertura
pytest --cov=app

# Modo verbose
pytest -v
```

**Cobertura:** 39 testes cobrindo:
- ✅ CRUD completo de filmes
- ✅ Busca e paginação
- ✅ Get-or-create de gêneros e diretores
- ✅ Adicionar reviews
- ✅ Cálculo de médias
- ✅ Validações
- ✅ Cascade delete

## Escala de Avaliação

- **Banco de Dados:** 0-10 (numérico)
- **Frontend:** Exibição em 5 estrelas (conversão automática: nota/2)
- **Input:** Usuário insere 0-10, frontend converte para estrelas para preview

## Variáveis de Ambiente

### Backend (`.env`)

```env
DATABASE_URL=sqlite:///./rocketlab.db
SEED_DATA_DIR_1=/home/lucas/DESAFIO/cinema/bases-1/bases_atv_dev1
SEED_DATA_DIR_2=/home/lucas/DESAFIO/cinema/bases-2/bases_atv_dev_2
LOG_LEVEL=INFO
```

### Frontend (`.env`)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Dados de Exemplo

Para popular o banco com dados iniciais:

```bash
cd backend
source .venv/bin/activate
python scripts/seed.py
```

Isso carrega:
- 95.645 filmes
- Gêneros, diretores, produtoras
- Reviews de exemplo
- Informações de performance (orçamento, receita, etc.)

## Troubleshooting

### Frontend não conecta ao backend
- Verifique se o backend está rodando: `http://localhost:8000`
- Valide a URL em `frontend/.env` → `VITE_API_URL`

### Erro "Filme não encontrado"
- Use `id_filme` (numérico curto) em URLs, não `sk_movie_id` (hash longo)
- Exemplo correto: `/movies/1018976` (id_filme)

### Títulos com caracteres estranhos
- A limpeza é automática na API (field validators Pydantic)
- Se aparecerem, limpe manualmente via scripts/seed.py

### Testes falhando
- Certifique-se de que Python 3.11+ está instalado
- Delete `pytest_cache/` e `.pytest_cache/`
- Rode: `pytest --tb=short`

## Performance

- **Paginação:** Limite padrão de 10 filmes/página
- **Busca:** Case-insensitive com índice de banco
- **Eager Loading:** Gêneros, diretores e reviews carregados juntamente
- **Caching:** Média de avaliações calculada em query-time (sempre atualizada)

## Contribuições & Próximos Passos (Opcional)

Possíveis melhorias:
- 🔐 Autenticação (JWT)
- 🏷️ Tags/Categorias adicionais
- ⭐ Ranking de filmes
- 💾 Cache Redis
- 📊 Análise de dados com gráficos
- 🔔 Notificações
- 📱 App mobile (React Native)
- 🎬 Streaming de trailers

## Licença

© 2026 Visagio - Rocket Lab. Todos os direitos reservados.
