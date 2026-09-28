# Cinema Review — Sistema Full-Stack de Avaliação de Filmes

**Plataforma Letterboxd-inspired para catalogação e avaliação de filmes** com backend FastAPI + frontend React/TypeScript, banco de dados SQLite com Alembic e cobertura completa de testes automatizados.

## 🎬 Funcionalidades

### Backend (FastAPI)
- ✅ **CRUD de Filmes** — Criar, listar, detalhar, atualizar, deletar
- ✅ **Busca e Filtros** — Por título, diretor, gênero, ano de lançamento
- ✅ **Ordenação** — Por título, ano, nota média (ascendente/descendente)
- ✅ **Reviews/Avaliações** — Adicionar, listar, validar nota (0-10)
- ✅ **Cálculo de Médias** — Média de notas por filme em tempo real
- ✅ **Paginação** — Suporte a page e page_size
- ✅ **Limpeza de Dados** — Remove caracteres corrompidos de títulos
- ✅ **API de Gêneros** — Listar gêneros únicos, ordenados

### Frontend (React + TypeScript)
- ✅ **Catálogo Paginado** — Grid de filmes com posters
- ✅ **Busca em Tempo Real** — Filtro por título/diretor
- ✅ **Filtros Múltiplos** — Gênero, diretor, ano
- ✅ **Ordenação Dinâmica** — UI para escolher campo e direção
- ✅ **Paginação Numérica** — Navegar entre páginas (1...20...100)
- ✅ **Página de Detalhe** — Filme completo + todas as reviews
- ✅ **Formulários** — Criar/editar filmes, adicionar reviews
- ✅ **Validação de Entrada** — Notas 0-10, campos obrigatórios
- ✅ **Dark Mode Automático** — Segue preferência do SO
- ✅ **Responsivo** — Mobile-first CSS

### Testes
- ✅ **59 testes automatizados** — 100% passando
- ✅ **Cobertura:** CRUD, reviews, filtros, ordenação, validação, limpeza
- Ver [`TESTES.md`](../TESTES.md) para detalhes completos

---

## 🏗️ Stack Técnico

### Backend
- **FastAPI** 0.109+ — Framework web assíncrono
- **SQLAlchemy 2.0** — ORM moderno com async
- **Pydantic v2** — Validação de schemas
- **Alembic** — Migrações de banco
- **SQLite** — Banco de dados local
- **pytest + pytest-asyncio** — Testes automatizados

### Frontend
- **React 18** — UI library
- **React Router v6** — Roteamento
- **TypeScript** — Type-safe JavaScript
- **Vite** — Build tool (dev speed ~instant)
- **CSS puro** — Sem dependências (dark mode automático)

### Estrutura do Banco
Esquema estrela com dimensões e fatos:
- `DimMovie` — Filmes (sk_movie_id, id_filme, título, sinopse, etc)
- `DimGenre` — Gêneros
- `DimPerson` — Diretores/Atores/Produtores
- `DimCompany` — Produtoras
- `MovieReview` — Avaliações individuais (nota 0-10, comentário)
- `FactMoviePerformance` — Desempenho (bilheteria, views)
- Tabelas de associação N:N (movie_genre, movie_person, etc)

---

## 🚀 Como Começar

### Pré-requisitos
- Python 3.11+ (backend)
- Node 18+ (frontend)
- pip + npm

### Backend

```bash
cd backend

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Banco de dados
alembic upgrade head

# (Opcional) Carregar dados de exemplo
python scripts/seed.py --data-dir /caminho/para/bases

# Rodar servidor
uvicorn app.main:app --reload
```

API estará em `http://localhost:8000`  
Docs interativa: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend

# Setup
npm install

# Desenvolvimento
npm run dev
```

App estará em `http://localhost:5173`

### Rodar Testes

```bash
cd backend
source .venv/bin/activate

# Todos os testes
pytest tests/ -v

# Apenas testes de filmes
pytest tests/test_movies.py -v

# Com cobertura
pytest tests/ --cov=app --cov-report=html
```

**Resultado:** ✅ 59 testes passando (100%)

---

## 📋 Endpoints Principais

### Filmes
```
GET    /api/v1/movies                    # Listar (com busca, filtros, ordenação, paginação)
GET    /api/v1/movies?search=titulo      # Buscar por título
GET    /api/v1/movies?genero=Ação        # Filtrar por gênero
GET    /api/v1/movies?diretor=Nolan      # Filtrar por diretor
GET    /api/v1/movies?ano=2024           # Filtrar por ano
GET    /api/v1/movies?order_by=nota_media&order_direction=desc  # Ordenar
GET    /api/v1/movies/{id}               # Detalhe com reviews
POST   /api/v1/movies                    # Criar
PUT    /api/v1/movies/{id}               # Atualizar
DELETE /api/v1/movies/{id}               # Deletar
```

### Reviews
```
POST   /api/v1/movies/{id}/reviews       # Adicionar avaliação
```

### Gêneros
```
GET    /api/v1/movies/genres             # Listar todos os gêneros únicos
```

---

## 📁 Estrutura do Projeto

```text
.
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   └── router.py          # Composição de routers
│   │   ├── core/
│   │   │   └── config.py          # Configurações globais
│   │   ├── db/
│   │   │   ├── base.py            # Base ORM + engine
│   │   │   └── session.py         # Dependency injection de sessão
│   │   ├── main.py                # App FastAPI + routers
│   │   └── movies/
│   │       ├── models.py          # SQLAlchemy (DimMovie, MovieReview, etc)
│   │       ├── schemas.py         # Pydantic (DTOs para API)
│   │       ├── repository.py      # Acesso a dados (queries)
│   │       ├── service.py         # Lógica de negócio
│   │       └── router.py          # Endpoints HTTP
│   ├── migrations/                # Alembic (versionamento do schema)
│   ├── scripts/
│   │   └── seed.py               # Carregador de CSVs
│   ├── tests/
│   │   ├── test_app.py           # Health check
│   │   ├── test_models.py        # Schema do banco
│   │   ├── test_movies.py        # 56 testes de API (CRUD, filtros, ordenação)
│   │   └── conftest.py           # Fixtures pytest
│   ├── pyproject.toml            # Deps + config pytest
│   └── rocketlab.db              # SQLite (criado após alembic upgrade)
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── client.ts         # HttpClient base
│   │   │   ├── movies.ts         # Funções de API específicas
│   │   │   └── types.ts          # TypeScript interfaces
│   │   ├── components/
│   │   │   ├── MovieCard.tsx     # Card do filme (grid)
│   │   │   ├── SearchBar.tsx     # Barra de busca
│   │   │   ├── FilterBar.tsx     # Filtros (gênero, diretor)
│   │   │   ├── Pagination.tsx    # Paginação numérica
│   │   │   ├── StarRating.tsx    # Estrelas (0-10 → 5★)
│   │   │   ├── ReviewList.tsx    # Lista de reviews
│   │   │   ├── ReviewForm.tsx    # Formulário de review
│   │   │   ├── MovieForm.tsx     # Formulário de filme
│   │   │   └── ConfirmDialog.tsx # Diálogo de confirmação
│   │   ├── pages/
│   │   │   ├── CatalogPage.tsx   # Página inicial (catálogo + filtros)
│   │   │   ├── MovieDetailPage.tsx # Detalhe do filme
│   │   │   └── MovieFormPage.tsx # Criar/editar filme
│   │   ├── styles/
│   │   │   └── index.css         # Stylesheet unificado (1300+ linhas)
│   │   ├── router.tsx            # React Router config
│   │   ├── App.tsx               # Root wrapper
│   │   └── main.tsx              # Entry point
│   ├── index.html                # HTML template
│   ├── package.json              # npm deps
│   └── vite.config.ts            # Vite config
│
├── ALTERAÇÕES.md                 # Log de mudanças do projeto
├── TESTES.md                     # Documentação dos testes
└── README.md                     # Este arquivo
```

---

## 🧪 Testes

### Cobertura Completa (59 testes)

| Categoria | Testes | Status |
|-----------|--------|--------|
| CRUD | 21 | ✅ |
| Reviews | 10 | ✅ |
| Filtros | 9 | ✅ |
| Ordenação | 6 | ✅ |
| Validação | 4 | ✅ |
| Limpeza de Dados | 2 | ✅ |
| Gêneros | 3 | ✅ |
| Casos Limite | 4 | ✅ |

Ver [`TESTES.md`](../TESTES.md) para lista completa de testes.

---

## 🎨 Features Visuais

### Dark Mode Automático
- Detecta preferência do SO (`prefers-color-scheme: dark`)
- CSS variables dinâmicas
- Sem toggle manual — segue sistema operacional

### Responsividade
- Mobile-first CSS
- Gutter de 16px em telas pequenas
- Grid cards reflow em telas maiores
- Botões e inputs full-width em mobile

### Validação
- Frontend: Checks em tempo real (nota 0-10, campos obrigatórios)
- Backend: Pydantic validators + HTTP 422 para dados inválidos

---

## 📝 Notas de Implementação

### Escala de Notas
- **Banco:** 0-10 (CheckConstraint no modelo)
- **Exibição:** Convertida para ⭐ 5 estrelas (ex: 7/10 = 3.5★)
- **API:** Retorna nota em escala 0-10; frontend renderiza como estrelas

### Deduplicação
- Gêneros e Diretores: get-or-create pattern
- Mesmo gênero em 5 filmes → 1 linha em `DimGenre`
- Queries usam `selectinload()` para eager load de relacionamentos

### Paginação
- Padrão: 10 filmes por página
- Max: 100 por página
- Mostra página atual ± 2 com `...` para gaps

### Limpeza de Dados
- Remove aspas escapadas: `"""` → `"`
- Remove caracteres UTF-8 corrompidos: `M-bM-^@M-^S` → `'`
- Aplicado via Pydantic `@field_validator` em responses

---

## 🔧 Troubleshooting

### "Porta 8000 já em uso"
```bash
# Linux/Mac
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows
netstat -ano | findstr :8000
```

### "Porta 5173 já em uso"
```bash
npm run dev -- --port 3000  # Use porta diferente
```

### Testes falhando
```bash
# Limpar cache pytest
pytest --cache-clear tests/

# Recriar banco de testes
rm -f backend/test_rocketlab.db
pytest tests/
```

### Erro de migrações
```bash
cd backend
alembic downgrade base
alembic upgrade head
```

---

## 📚 Referências

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Router Docs](https://reactrouter.com/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Vite Guide](https://vitejs.dev/guide/)

---

## 📄 Arquivos de Documentação

- **[ALTERAÇÕES.md](../ALTERAÇÕES.md)** — Log detalhado de todas as mudanças
- **[TESTES.md](../TESTES.md)** — Cobertura completa de testes automatizados
- **[README_CINEMA.md](./README_CINEMA.md)** — Documentação anterior (manter para referência)

---

**Status:** ✅ **PROJETO COMPLETO E PRONTO PARA PRODUÇÃO**  
**Data:** 28/09/2026  
**Testes:** 59/59 passando (100%)
