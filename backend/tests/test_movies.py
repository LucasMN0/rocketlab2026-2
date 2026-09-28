"""Testes automatizados da API de filmes."""

import pytest
from sqlalchemy import func, select

# AJUSTE: mesmo módulo importado no conftest.py
from app.movies.models import DimGenre, DimPerson, MovieReview

pytestmark = pytest.mark.asyncio

# AJUSTE: prefixo usado no include_router do main.py ("" se não houver)
API = "/api/v1"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def criar_filme(client, **overrides) -> dict:
    payload = {
        "titulo": "Filme Teste",
        "diretor": "Diretor Teste",
        "ano_lancamento": 2024,
        "genero": "Ação",
        "sinopse": "Uma sinopse legal",
    }
    payload.update(overrides)
    response = await client.post(f"{API}/movies", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


async def criar_review(client, movie_id: str, nota: float, nome: str = "João Silva"):
    return await client.post(
        f"{API}/movies/{movie_id}/reviews",
        json={"nome": nome, "nota": nota, "comentario": "Comentário de teste"},
    )


async def contar(session_factory, stmt) -> int:
    async with session_factory() as session:
        return await session.scalar(stmt)


# ---------------------------------------------------------------------------
# GET /movies
# ---------------------------------------------------------------------------

async def test_listar_filmes_retorna_200(client):
    response = await client.get(f"{API}/movies")
    assert response.status_code == 200


async def test_listar_filmes_retorna_estrutura_paginada(client):
    await criar_filme(client)

    body = (await client.get(f"{API}/movies")).json()

    assert set(body) >= {"items", "total", "page", "page_size", "pages"}
    assert body["page"] == 1
    assert body["page_size"] == 10


async def test_busca_filtra_por_titulo(client):
    await criar_filme(client, titulo="The Matrix")
    await criar_filme(client, titulo="Matrix Reloaded")
    await criar_filme(client, titulo="Amélie")

    body = (await client.get(f"{API}/movies", params={"search": "Matrix"})).json()

    assert body["total"] == 2
    assert all("matrix" in item["titulo"].lower() for item in body["items"])


async def test_busca_inexistente_retorna_vazio(client):
    await criar_filme(client)

    body = (await client.get(f"{API}/movies", params={"search": "XYZ123"})).json()

    assert body["items"] == []
    assert body["total"] == 0


async def test_paginacao_retorna_paginas_diferentes(client):
    for i in range(15):
        await criar_filme(client, titulo=f"Filme {i:02d}")

    pagina1 = (await client.get(f"{API}/movies", params={"page": 1})).json()
    pagina2 = (await client.get(f"{API}/movies", params={"page": 2})).json()

    assert pagina1["total"] == 15
    assert pagina1["pages"] == 2
    assert len(pagina1["items"]) == 10
    assert len(pagina2["items"]) == 5

    ids1 = {m["sk_movie_id"] for m in pagina1["items"]}
    ids2 = {m["sk_movie_id"] for m in pagina2["items"]}
    assert ids1.isdisjoint(ids2)


# ---------------------------------------------------------------------------
# GET /movies/{id}
# ---------------------------------------------------------------------------

async def test_detalhe_filme_existente(client):
    filme = await criar_filme(client, titulo="The Matrix", duracao_minutos=136)

    response = await client.get(f"{API}/movies/{filme['sk_movie_id']}")

    assert response.status_code == 200
    body = response.json()
    assert body["titulo"] == "The Matrix"
    assert body["diretor"] == "Diretor Teste"
    assert body["genero"] == "Ação"
    assert body["duracao_minutos"] == 136
    assert body["reviews"] == []
    assert body["qtd_avaliacoes"] == 0


async def test_detalhe_filme_inexistente_retorna_404(client):
    response = await client.get(f"{API}/movies/id-que-nao-existe")
    assert response.status_code == 404


async def test_detalhe_inclui_todas_as_reviews(client):
    filme = await criar_filme(client)
    await criar_review(client, filme["sk_movie_id"], 8, nome="Ana")
    await criar_review(client, filme["sk_movie_id"], 9, nome="Bruno")

    body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()

    assert len(body["reviews"]) == 2
    assert {r["nome"] for r in body["reviews"]} == {"Ana", "Bruno"}


async def test_nota_media_calculada_corretamente(client):
    filme = await criar_filme(client)
    for nota in (8, 9, 7):
        await criar_review(client, filme["sk_movie_id"], nota)

    body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()

    assert body["nota_media"] == pytest.approx(8.0)
    assert body["qtd_avaliacoes"] == 3


# ---------------------------------------------------------------------------
# POST /movies
# ---------------------------------------------------------------------------

async def test_criar_filme_retorna_201(client):
    response = await client.post(
        f"{API}/movies",
        json={
            "titulo": "Meu Filme",
            "diretor": "Diretor Novo",
            "ano_lancamento": 2024,
            "genero": "Ação",
        },
    )
    assert response.status_code == 201
    assert response.json()["sk_movie_id"]


async def test_filme_criado_aparece_na_listagem(client):
    filme = await criar_filme(client, titulo="Meu Filme")

    body = (await client.get(f"{API}/movies")).json()

    assert filme["sk_movie_id"] in {m["sk_movie_id"] for m in body["items"]}


async def test_filme_criado_retorna_dados_corretos_no_detalhe(client):
    filme = await criar_filme(
        client, titulo="Meu Filme", ano_lancamento=2020, sinopse="Texto"
    )

    body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()

    assert body["titulo"] == "Meu Filme"
    assert body["ano_lancamento"] == 2020
    assert body["sinopse"] == "Texto"
    assert body["genero"] == "Ação"
    assert body["diretor"] == "Diretor Teste"


async def test_mesmo_genero_nao_duplica(client, session_factory):
    await criar_filme(client, titulo="Filme A", genero="Ação")
    await criar_filme(client, titulo="Filme B", genero="Ação")

    total = await contar(
        session_factory,
        select(func.count()).select_from(DimGenre).where(DimGenre.nome_genero == "Ação"),
    )
    assert total == 1


async def test_mesmo_diretor_nao_duplica(client, session_factory):
    await criar_filme(client, titulo="Filme A", diretor="Christopher Nolan")
    await criar_filme(client, titulo="Filme B", diretor="Christopher Nolan")

    total = await contar(
        session_factory,
        select(func.count())
        .select_from(DimPerson)
        .where(
            DimPerson.nome_pessoa == "Christopher Nolan",
            DimPerson.tipo_pessoa == "Diretor",
        ),
    )
    assert total == 1


@pytest.mark.parametrize("campo", ["titulo", "diretor", "ano_lancamento", "genero"])
async def test_criar_sem_campo_obrigatorio_retorna_422(client, campo):
    payload = {
        "titulo": "Meu Filme",
        "diretor": "Diretor",
        "ano_lancamento": 2024,
        "genero": "Ação",
    }
    del payload[campo]

    response = await client.post(f"{API}/movies", json=payload)

    assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /movies/{id}
# ---------------------------------------------------------------------------

async def test_atualizar_filme_retorna_200(client):
    filme = await criar_filme(client)

    response = await client.put(
        f"{API}/movies/{filme['sk_movie_id']}", json={"titulo": "Novo Título"}
    )

    assert response.status_code == 200


async def test_atualizar_so_titulo_mantem_outros_campos(client):
    filme = await criar_filme(client, ano_lancamento=2010, sinopse="Original")

    await client.put(f"{API}/movies/{filme['sk_movie_id']}", json={"titulo": "Novo Título"})
    body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()

    assert body["titulo"] == "Novo Título"
    assert body["diretor"] == "Diretor Teste"
    assert body["genero"] == "Ação"
    assert body["ano_lancamento"] == 2010
    assert body["sinopse"] == "Original"


async def test_atualizar_todos_os_campos(client):
    filme = await criar_filme(client)
    novos = {
        "titulo": "Novo Título",
        "diretor": "Novo Diretor",
        "ano_lancamento": 2025,
        "genero": "Ficção Científica",
        "sinopse": "Nova sinopse",
        "duracao_minutos": 120,
    }

    await client.put(f"{API}/movies/{filme['sk_movie_id']}", json=novos)
    body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()

    for campo, valor in novos.items():
        assert body[campo] == valor


async def test_atualizar_filme_inexistente_retorna_404(client):
    response = await client.put(
        f"{API}/movies/id-que-nao-existe", json={"titulo": "Qualquer"}
    )
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /movies/{id}
# ---------------------------------------------------------------------------

async def test_deletar_filme_retorna_204(client):
    filme = await criar_filme(client)

    response = await client.delete(f"{API}/movies/{filme['sk_movie_id']}")

    assert response.status_code == 204


async def test_filme_deletado_desaparece(client):
    filme = await criar_filme(client)

    await client.delete(f"{API}/movies/{filme['sk_movie_id']}")

    detalhe = await client.get(f"{API}/movies/{filme['sk_movie_id']}")
    lista = (await client.get(f"{API}/movies")).json()
    assert detalhe.status_code == 404
    assert filme["sk_movie_id"] not in {m["sk_movie_id"] for m in lista["items"]}


async def test_deletar_filme_remove_reviews_em_cascata(client, session_factory):
    filme = await criar_filme(client)
    await criar_review(client, filme["sk_movie_id"], 8)
    await criar_review(client, filme["sk_movie_id"], 6)

    await client.delete(f"{API}/movies/{filme['sk_movie_id']}")

    total = await contar(
        session_factory,
        select(func.count())
        .select_from(MovieReview)
        .where(MovieReview.sk_movie_id == filme["sk_movie_id"]),
    )
    assert total == 0


async def test_deletar_filme_inexistente_retorna_404(client):
    response = await client.delete(f"{API}/movies/id-que-nao-existe")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /movies/{id}/reviews
# ---------------------------------------------------------------------------

async def test_adicionar_review_retorna_201(client):
    filme = await criar_filme(client)

    response = await criar_review(client, filme["sk_movie_id"], 8.5)

    assert response.status_code == 201
    body = response.json()
    assert body["nota"] == pytest.approx(8.5)
    assert body["sk_movie_review_id"]


async def test_review_aparece_no_detalhe(client):
    filme = await criar_filme(client)
    review = (await criar_review(client, filme["sk_movie_id"], 7)).json()

    body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()

    assert review["sk_movie_review_id"] in {
        r["sk_movie_review_id"] for r in body["reviews"]
    }


async def test_nota_media_recalcula_apos_nova_review(client):
    filme = await criar_filme(client)
    url = f"{API}/movies/{filme['sk_movie_id']}"

    await criar_review(client, filme["sk_movie_id"], 10)
    assert (await client.get(url)).json()["nota_media"] == pytest.approx(10.0)

    await criar_review(client, filme["sk_movie_id"], 6)
    body = (await client.get(url)).json()
    assert body["nota_media"] == pytest.approx(8.0)
    assert body["qtd_avaliacoes"] == 2


@pytest.mark.parametrize("nota", [0, 10])
async def test_notas_nos_limites_sao_aceitas(client, nota):
    filme = await criar_filme(client)

    response = await criar_review(client, filme["sk_movie_id"], nota)

    assert response.status_code == 201


@pytest.mark.parametrize("nota", [-5, -0.1, 10.1, 15])
async def test_nota_fora_do_intervalo_retorna_422(client, nota):
    filme = await criar_filme(client)

    response = await criar_review(client, filme["sk_movie_id"], nota)

    assert response.status_code == 422


async def test_review_em_filme_inexistente_retorna_404(client):
    response = await criar_review(client, "id-que-nao-existe", 8)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Integração (fluxos completos)
# ---------------------------------------------------------------------------

async def test_fluxo_criar_avaliar_deletar(client):
    filme = await criar_filme(client, titulo="Fluxo Completo")
    movie_id = filme["sk_movie_id"]

    for nota in (8, 9, 7):
        assert (await criar_review(client, movie_id, nota)).status_code == 201

    body = (await client.get(f"{API}/movies/{movie_id}")).json()
    assert body["nota_media"] == pytest.approx(8.0)
    assert len(body["reviews"]) == 3

    assert (await client.delete(f"{API}/movies/{movie_id}")).status_code == 204
    assert (await client.get(f"{API}/movies/{movie_id}")).status_code == 404


async def test_fluxo_dois_filmes_mesmo_genero(client, session_factory):
    a = await criar_filme(client, titulo="Filme A", genero="Drama")
    b = await criar_filme(client, titulo="Filme B", genero="Drama")

    total = await contar(
        session_factory,
        select(func.count()).select_from(DimGenre).where(DimGenre.nome_genero == "Drama"),
    )
    assert total == 1

    for filme in (a, b):
        body = (await client.get(f"{API}/movies/{filme['sk_movie_id']}")).json()
        assert body["genero"] == "Drama"


async def test_trocar_diretor_nao_apaga_diretor_antigo(client, session_factory):
    a = await criar_filme(client, titulo="Filme A", diretor="Diretor Antigo")
    b = await criar_filme(client, titulo="Filme B", diretor="Diretor Antigo")

    await client.put(f"{API}/movies/{a['sk_movie_id']}", json={"diretor": "Diretor Novo"})

    total_antigo = await contar(
        session_factory,
        select(func.count())
        .select_from(DimPerson)
        .where(
            DimPerson.nome_pessoa == "Diretor Antigo",
            DimPerson.tipo_pessoa == "Diretor",
        ),
    )
    assert total_antigo == 1

    body_a = (await client.get(f"{API}/movies/{a['sk_movie_id']}")).json()
    body_b = (await client.get(f"{API}/movies/{b['sk_movie_id']}")).json()
    assert body_a["diretor"] == "Diretor Novo"
    assert body_b["diretor"] == "Diretor Antigo"