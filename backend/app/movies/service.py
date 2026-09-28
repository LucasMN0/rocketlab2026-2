"""Camada de serviço para regras de negócio de filmes."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.movies.models import DimMovie
from app.movies.repository import (
    add_review,
    create_movie,
    delete_movie,
    get_movie_by_id,
    get_or_create_director,
    get_or_create_genre,
    get_review_stats,
    list_movies,
    update_movie,
)
from app.movies.schemas import (
    MovieCreate,
    MovieDetail,
    MovieListItem,
    MovieUpdate,
    ReviewCreate,
    ReviewOut,
)


class MovieNotFoundError(Exception):
    """Exceção lançada quando um filme não é encontrado."""

    pass


async def list_movies_with_stats(
    session: AsyncSession, search: str | None = None, page: int = 1, page_size: int = 10
) -> tuple[list[MovieListItem], int]:
    """Lista filmes com suas estatísticas de avaliação."""
    movies, total = await list_movies(session, search, page, page_size)

    items = []
    for movie in movies:
        nota_media, qtd = await get_review_stats(session, movie.sk_movie_id)

        diretor = None
        if movie.people:
            for p in movie.people:
                if p.tipo_pessoa == "Diretor":
                    diretor = p.nome_pessoa
                    break

        genero = movie.genres[0].nome_genero if movie.genres else None

        item = MovieListItem(
            sk_movie_id=movie.sk_movie_id,
            titulo=movie.titulo,
            ano_lancamento=movie.ano_lancamento,
            genero=genero,
            diretor=diretor,
            url_poster=movie.url_poster,
            nota_media=nota_media,
            qtd_avaliacoes=qtd,
        )
        items.append(item)

    return items, total


async def get_movie_detail(session: AsyncSession, movie_id: str) -> MovieDetail:
    """Obtém detalhes de um filme com suas avaliações e estatísticas."""
    movie = await get_movie_by_id(session, movie_id)
    if not movie:
        raise MovieNotFoundError(f"Filme {movie_id} não encontrado")

    nota_media, qtd = await get_review_stats(session, movie.sk_movie_id)

    diretor = None
    if movie.people:
        for p in movie.people:
            if p.tipo_pessoa == "Diretor":
                diretor = p.nome_pessoa
                break

    genero = movie.genres[0].nome_genero if movie.genres else None

    reviews = [
        ReviewOut(
            sk_movie_review_id=r.sk_movie_review_id,
            nome=r.nome,
            nota=r.nota,
            comentario=r.comentario,
            created_at=r.created_at,
        )
        for r in sorted(movie.reviews, key=lambda x: x.created_at, reverse=True)
    ]

    return MovieDetail(
        sk_movie_id=movie.sk_movie_id,
        titulo=movie.titulo,
        ano_lancamento=movie.ano_lancamento,
        duracao_minutos=movie.duracao_minutos,
        sinopse=movie.sinopse,
        genero=genero,
        diretor=diretor,
        url_poster=movie.url_poster,
        url_backdrop=movie.url_backdrop,
        nota_media=nota_media,
        qtd_avaliacoes=qtd,
        reviews=reviews,
    )


async def create_movie_service(session: AsyncSession, data: MovieCreate) -> MovieDetail:
    """Cria um novo filme com seus relacionamentos."""
    genre = await get_or_create_genre(session, data.genero)
    director = await get_or_create_director(session, data.diretor)

    movie = DimMovie(
        titulo=data.titulo,
        ano_lancamento=data.ano_lancamento,
        sinopse=data.sinopse,
        duracao_minutos=data.duracao_minutos,
        url_poster=data.url_poster,
    )
    movie.genres.append(genre)
    movie.people.append(director)

    movie = await create_movie(session, movie)
    await session.commit()
    await session.refresh(movie)

    return await get_movie_detail(session, movie.sk_movie_id)


async def update_movie_service(
    session: AsyncSession, movie_id: str, data: MovieUpdate
) -> MovieDetail:
    """Atualiza um filme."""
    movie = await get_movie_by_id(session, movie_id)
    if not movie:
        raise MovieNotFoundError(f"Filme {movie_id} não encontrado")

    updates = data.model_dump(exclude_unset=True, exclude={"genero", "diretor"})

    if data.genero:
        genre = await get_or_create_genre(session, data.genero)
        movie.genres = [genre]

    if data.diretor:
        director = await get_or_create_director(session, data.diretor)
        movie.people = [p for p in movie.people if p.tipo_pessoa != "Diretor"]
        movie.people.append(director)

    movie = await update_movie(session, movie, updates)
    await session.commit()
    await session.refresh(movie)

    return await get_movie_detail(session, movie.sk_movie_id)


async def delete_movie_service(session: AsyncSession, movie_id: str) -> None:
    """Deleta um filme."""
    movie = await get_movie_by_id(session, movie_id)
    if not movie:
        raise MovieNotFoundError(f"Filme {movie_id} não encontrado")

    await delete_movie(session, movie)
    await session.commit()


async def add_review_service(
    session: AsyncSession, movie_id: str, data: ReviewCreate
) -> ReviewOut:
    """Adiciona uma nova avaliação a um filme."""
    movie = await get_movie_by_id(session, movie_id)
    if not movie:
        raise MovieNotFoundError(f"Filme {movie_id} não encontrado")

    review = await add_review(session, movie_id, data.nome, data.nota, data.comentario)
    await session.commit()
    await session.refresh(review)

    return ReviewOut(
        sk_movie_review_id=review.sk_movie_review_id,
        nome=review.nome,
        nota=review.nota,
        comentario=review.comentario,
        created_at=review.created_at,
    )
