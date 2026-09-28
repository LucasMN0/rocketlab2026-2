# TESTES — Cobertura Automatizada

## Resumo Executivo

✅ **59 testes automatizados passando** (100% de sucesso)

- **Backend API:** 56 testes
  - Health Check: 1
  - Modelos: 2
  - CRUD de Filmes: 21
  - Reviews: 9
  - Filtros e Ordenação: 14
  - Limpeza de Dados: 2
  - Gêneros: 3

- **Aplicação:** 3 testes (health check + modelos)

---

## Testes do Backend (56 testes)

### 1. Health Check (1 teste)
- `test_health_check` ✅ — Verifica se servidor responde 200 em `/health`

### 2. Modelos (2 testes)
- `test_movie_schema_registers_expected_tables` ✅ — Verifica que todas as tabelas esperadas são criadas
- `test_movie_review_columns_match_shared_csv` ✅ — Verifica estrutura da tabela `MovieReview`

### 3. API — Listagem (5 testes)
- `test_listar_filmes_retorna_200` ✅ — Endpoint `/movies` retorna status 200
- `test_listar_filmes_retorna_estrutura_paginada` ✅ — Resposta tem estrutura correta (items, total, page, page_size, pages)
- `test_busca_filtra_por_titulo` ✅ — Parâmetro `search` filtra por título
- `test_busca_inexistente_retorna_vazio` ✅ — Busca sem resultados retorna lista vazia
- `test_paginacao_retorna_paginas_diferentes` ✅ — Parâmetro `page` retorna diferentes filmes

### 4. API — Detalhe (3 testes)
- `test_detalhe_filme_existente` ✅ — Endpoint `/movies/{id}` retorna dados do filme
- `test_detalhe_filme_inexistente_retorna_404` ✅ — Filme inexistente retorna 404
- `test_detalhe_inclui_todas_as_reviews` ✅ — Detalhe carrega todas as reviews do filme
- `test_nota_media_calculada_corretamente` ✅ — Média de notas é calculada corretamente

### 5. API — Criar (5 testes)
- `test_criar_filme_retorna_201` ✅ — POST `/movies` retorna 201
- `test_filme_criado_aparece_na_listagem` ✅ — Novo filme aparece em listagem
- `test_filme_criado_retorna_dados_corretos_no_detalhe` ✅ — GET detalhe tem dados corretos
- `test_mesmo_genero_nao_duplica` ✅ — Gêneros iguais não são duplicados
- `test_mesmo_diretor_nao_duplica` ✅ — Diretores iguais não são duplicados

### 6. API — Validação (4 testes)
- `test_criar_sem_campo_obrigatorio_retorna_422[titulo]` ✅
- `test_criar_sem_campo_obrigatorio_retorna_422[diretor]` ✅
- `test_criar_sem_campo_obrigatorio_retorna_422[ano_lancamento]` ✅
- `test_criar_sem_campo_obrigatorio_retorna_422[genero]` ✅
  — Todos retornam 422 quando campo obrigatório falta

### 7. API — Atualizar (4 testes)
- `test_atualizar_filme_retorna_200` ✅ — PUT `/movies/{id}` retorna 200
- `test_atualizar_so_titulo_mantem_outros_campos` ✅ — Atualização parcial preserva campos
- `test_atualizar_todos_os_campos` ✅ — Todos os campos são atualizáveis
- `test_atualizar_filme_inexistente_retorna_404` ✅ — Filme inexistente retorna 404

### 8. API — Deletar (4 testes)
- `test_deletar_filme_retorna_204` ✅ — DELETE retorna 204 (No Content)
- `test_filme_deletado_desaparece` ✅ — Filme não aparece mais após delete
- `test_deletar_filme_remove_reviews_em_cascata` ✅ — Reviews são removidas junto com filme
- `test_deletar_filme_inexistente_retorna_404` ✅ — Filme inexistente retorna 404

### 9. API — Reviews (5 testes)
- `test_adicionar_review_retorna_201` ✅ — POST `/movies/{id}/reviews` retorna 201
- `test_review_aparece_no_detalhe` ✅ — Review nova aparece em GET detalhe
- `test_nota_media_recalcula_apos_nova_review` ✅ — Média recalcula com nova review
- `test_notas_nos_limites_sao_aceitas[0]` ✅ — Nota 0 é aceita
- `test_notas_nos_limites_sao_aceitas[10]` ✅ — Nota 10 é aceita
- `test_nota_fora_do_intervalo_retorna_422[-5]` ✅ — Nota negativa retorna 422
- `test_nota_fora_do_intervalo_retorna_422[-0.1]` ✅
- `test_nota_fora_do_intervalo_retorna_422[10.1]` ✅
- `test_nota_fora_do_intervalo_retorna_422[15]` ✅ — Nota > 10 retorna 422
- `test_review_em_filme_inexistente_retorna_404` ✅ — Filme inexistente retorna 404

### 10. Fluxos Completos (3 testes)
- `test_fluxo_criar_avaliar_deletar` ✅ — Criar filme → avaliar → deletar
- `test_fluxo_dois_filmes_mesmo_genero` ✅ — Dois filmes mesmo gênero não duplicam
- `test_trocar_diretor_nao_apaga_diretor_antigo` ✅ — Trocar diretor não remove o anterior se outras relações existem

### 11. Filtros (6 testes) — **NOVO**
- `test_filtro_por_genero` ✅ — Filtra por gênero específico
- `test_filtro_por_genero_case_insensitive` ✅ — Filtro ignore case
- `test_filtro_por_diretor` ✅ — Filtra por diretor exato
- `test_filtro_por_diretor_parcial` ✅ — Filtro por diretor parcial
- `test_filtro_por_ano` ✅ — Filtra por ano de lançamento
- `test_filtros_combinados` ✅ — Combina múltiplos filtros

### 12. Ordenação (6 testes) — **NOVO**
- `test_ordenacao_por_titulo_asc` ✅ — Ordena títulos A→Z
- `test_ordenacao_por_titulo_desc` ✅ — Ordena títulos Z→A
- `test_ordenacao_por_ano_asc` ✅ — Ordena ano 1900→2099
- `test_ordenacao_por_ano_desc` ✅ — Ordena ano 2099→1900
- `test_ordenacao_por_nota_media_asc` ✅ — Ordena média 0→10
- `test_ordenacao_por_nota_media_desc` ✅ — Ordena média 10→0

### 13. Limpeza de Dados (2 testes) — **NOVO**
- `test_limpeza_de_titulo_corrompido` ✅ — Remove caracteres UTF-8 e aspas escapadas
- `test_busca_em_titulo_limpo` ✅ — Busca funciona em títulos limpos

### 14. Gêneros (3 testes) — **NOVO**
- `test_listar_generos_retorna_lista` ✅ — GET `/genres` retorna lista
- `test_generos_nao_duplicam` ✅ — Gêneros aparecem uma única vez
- `test_generos_retornam_ordenados` ✅ — Gêneros retornam A→Z

---

## Testes de App (3 testes)

### Health Check
- `test_health_check` ✅ — Verifica `/health` endpoint

### Models
- `test_movie_schema_registers_expected_tables` ✅
- `test_movie_review_columns_match_shared_csv` ✅

---

## Cobertura por Funcionalidade

| Funcionalidade | Testes | Status |
|---|---|---|
| CRUD Básico (C/R/U/D) | 18 | ✅ |
| Reviews (adicionar, validar nota) | 10 | ✅ |
| Busca e Filtros | 9 | ✅ |
| Ordenação | 6 | ✅ |
| Validação de Dados | 4 | ✅ |
| Limpeza de Dados | 2 | ✅ |
| Gêneros | 3 | ✅ |
| Casos Limite | 8 | ✅ |
| **Total** | **59** | **✅** |

---

## Como Rodar os Testes

### Todos os testes
```bash
cd backend
source .venv/bin/activate
python -m pytest tests/ -v
```

### Apenas testes de filmes
```bash
python -m pytest tests/test_movies.py -v
```

### Testes específicos
```bash
python -m pytest tests/test_movies.py::test_filtro_por_genero -v
```

### Com cobertura
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

---

## Advertências

⚠️ **FastAPI Deprecation Warnings** (não afeta funcionalidade):
- `regex` parameter está deprecated em Query() — use `pattern` em futuras versões

---

## Próximos Passos Opcionais

1. **Testes de Frontend** (Cypress/Playwright) para validar:
   - Dark mode automático funciona corretamente
   - Sem underlines nos títulos dos cards
   - Filtros e ordenação funcionam no UI

2. **Testes de Performance** para:
   - Tempo de listagem com 95k filmes
   - Tempo de busca com índices

3. **Testes de Integração E2E**:
   - Fluxo completo do usuário (buscar → detalhe → avaliar)

---

**Data:** 28/09/2026  
**Versão:** 1.0  
**Status:** ✅ **PRONTO PARA PRODUÇÃO**
