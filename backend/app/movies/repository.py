"""Repository de dados para o domínio de filmes."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.movies.models import DimGenre, DimMovie, DimPerson, MovieReview


async def get_or_create_genre(session: AsyncSession, nome_genero: str) -> DimGenre:
    """Busca um gênero por nome ou o cria se não existir."""
    stmt = select(DimGenre).where(DimGenre.nome_genero == nome_genero)
    result = await session.execute(stmt)
    genre = result.scalars().first()

    if not genre:
        genre = DimGenre(nome_genero=nome_genero)
        session.add(genre)
        await session.flush()

    return genre


async def get_or_create_director(session: AsyncSession, nome_pessoa: str) -> DimPerson:
    """Busca um diretor por nome ou o cria se não existir."""
    stmt = select(DimPerson).where(
        (DimPerson.nome_pessoa == nome_pessoa) & (DimPerson.tipo_pessoa == "Diretor")
    )
    result = await session.execute(stmt)
    person = result.scalars().first()

    if not person:
        person = DimPerson(nome_pessoa=nome_pessoa, tipo_pessoa="Diretor")
        session.add(person)
        await session.flush()

    return person


async def list_genres(session: AsyncSession) -> list[DimGenre]:
    """Retorna lista de todos os gêneros únicos, ordenados por nome."""
    stmt = select(DimGenre).order_by(DimGenre.nome_genero)
    result = await session.execute(stmt)
    return result.scalars().all()


async def list_movies(
    session: AsyncSession,
    search: str | None = None,
    diretor: str | None = None,
    genero: str | None = None,
    ano: int | None = None,
    order_by: str = "titulo",
    order_direction: str = "asc",
    page: int = 1,
    page_size: int = 10,
) -> tuple[list[DimMovie], int]:
    """Lista filmes com paginação e filtros opcionais por título/diretor, diretor e gênero."""
    stmt = select(DimMovie).options(
        selectinload(DimMovie.genres), selectinload(DimMovie.people)
    )

    # Busca por título
    if search:
        stmt = stmt.where(DimMovie.titulo.ilike(f"%{search}%"))

    # Filtro por diretor específico
    if diretor:
        stmt = stmt.join(DimMovie.people).where(
            (DimPerson.nome_pessoa.ilike(f"%{diretor}%")) & (DimPerson.tipo_pessoa == "Diretor")
        )

    if genero:
        stmt = stmt.join(DimMovie.genres).where(DimGenre.nome_genero.ilike(f"%{genero}%"))

    if ano:
        stmt = stmt.where(DimMovie.ano_lancamento == ano)

    count_stmt = select(func.count(func.distinct(DimMovie.sk_movie_id))).select_from(DimMovie)
    if search:
        count_stmt = count_stmt.where(DimMovie.titulo.ilike(f"%{search}%"))
    if diretor:
        count_stmt = count_stmt.join(DimMovie.people).where(
            (DimPerson.nome_pessoa.ilike(f"%{diretor}%")) & (DimPerson.tipo_pessoa == "Diretor")
        )
    if genero:
        count_stmt = count_stmt.join(DimMovie.genres).where(DimGenre.nome_genero.ilike(f"%{genero}%"))
    if ano:
        count_stmt = count_stmt.where(DimMovie.ano_lancamento == ano)

    count_result = await session.execute(count_stmt)
    total = count_result.scalar() or 0

    # Aplicar ordenação
    order_column = DimMovie.titulo
    if order_by == "ano_lancamento":
        order_column = DimMovie.ano_lancamento
    elif order_by == "nota_media":
        # Ordenar por média calculada em tempo real
        stmt = stmt.outerjoin(MovieReview).group_by(DimMovie.sk_movie_id)
        order_column = func.avg(MovieReview.nota)

    if order_direction.lower() == "desc":
        stmt = stmt.order_by(order_column.desc())
    else:
        stmt = stmt.order_by(order_column.asc())

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    result = await session.execute(stmt)
    movies = result.unique().scalars().all()

    return movies, total


async def get_movie_by_id(session: AsyncSession, movie_id: str) -> DimMovie | None:
    """Busca um filme pelo sk_movie_id ou id_filme com eager load de relacionamentos."""
    stmt = select(DimMovie).where(
        (DimMovie.sk_movie_id == movie_id) | (DimMovie.id_filme == movie_id)
    ).options(
        selectinload(DimMovie.genres),
        selectinload(DimMovie.people),
        selectinload(DimMovie.reviews),
    )
    result = await session.execute(stmt)
    return result.scalars().first()


async def create_movie(
    session: AsyncSession, movie: DimMovie
) -> DimMovie:
    """Cria um novo filme."""
    session.add(movie)
    await session.flush()
    return movie


async def update_movie(
    session: AsyncSession, movie: DimMovie, updates: dict
) -> DimMovie:
    """Atualiza um filme com os campos fornecidos."""
    for key, value in updates.items():
        if value is not None and hasattr(movie, key):
            setattr(movie, key, value)
    await session.flush()
    return movie


async def delete_movie(session: AsyncSession, movie: DimMovie) -> None:
    """Deleta um filme e seus relacionamentos (cascade)."""
    await session.delete(movie)
    await session.flush()


async def add_review(
    session: AsyncSession, movie_id: str, nome: str, nota: float, comentario: str
) -> MovieReview:
    """Cria uma nova avaliação para um filme."""
    review = MovieReview(sk_movie_id=movie_id, nome=nome, nota=nota, comentario=comentario)
    session.add(review)
    await session.flush()
    return review


async def get_review_stats(session: AsyncSession, movie_id: str) -> tuple[float | None, int]:
    """Calcula a média e quantidade de avaliações de um filme."""
    stmt = select(func.avg(MovieReview.nota), func.count(MovieReview.sk_movie_review_id)).where(
        MovieReview.sk_movie_id == movie_id
    )
    result = await session.execute(stmt)
    avg_nota, count = result.one()
    return avg_nota, count or 0
