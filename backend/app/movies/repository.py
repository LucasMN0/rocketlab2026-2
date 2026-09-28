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


async def list_movies(
    session: AsyncSession, search: str | None = None, page: int = 1, page_size: int = 10
) -> tuple[list[DimMovie], int]:
    """Lista filmes com paginação e busca opcional por título."""
    stmt = select(DimMovie).options(
        selectinload(DimMovie.genres), selectinload(DimMovie.people), selectinload(DimMovie.reviews)
    )

    if search:
        stmt = stmt.where(DimMovie.titulo.ilike(f"%{search}%"))

    count_stmt = select(func.count()).select_from(DimMovie)
    if search:
        count_stmt = count_stmt.where(DimMovie.titulo.ilike(f"%{search}%"))

    count_result = await session.execute(count_stmt)
    total = count_result.scalar()

    stmt = stmt.offset((page - 1) * page_size).limit(page_size).order_by(DimMovie.titulo)
    result = await session.execute(stmt)
    movies = result.unique().scalars().all()

    return movies, total


async def get_movie_by_id(session: AsyncSession, movie_id: str) -> DimMovie | None:
    """Busca um filme pelo ID com eager load de relacionamentos."""
    stmt = select(DimMovie).where(DimMovie.sk_movie_id == movie_id).options(
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
