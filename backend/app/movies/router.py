"""Endpoints da API de filmes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.movies.repository import list_genres
from app.movies.schemas import (
    GenreList,
    MovieCreate,
    MovieDetail,
    MovieUpdate,
    PaginatedMovies,
    ReviewCreate,
    ReviewOut,
)
from app.movies.service import (
    MovieNotFoundError,
    add_review_service,
    create_movie_service,
    delete_movie_service,
    get_movie_detail,
    list_movies_with_stats,
    update_movie_service,
)

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=PaginatedMovies)
async def list_movies(
    search: str | None = Query(None, min_length=1, description="Buscar por título"),
    diretor: str | None = Query(None, min_length=1, description="Filtrar por diretor"),
    genero: str | None = Query(None, min_length=1, description="Filtrar por gênero"),
    ano: int | None = Query(None, ge=1900, le=2100, description="Filtrar por ano de lançamento"),
    order_by: str = Query("titulo", regex="^(titulo|ano_lancamento|nota_media)$", description="Campo para ordenação"),
    order_direction: str = Query("asc", regex="^(asc|desc)$", description="Direção da ordenação"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
) -> PaginatedMovies:
    """Lista filmes com paginação e filtros opcionais (título, diretor, gênero, ano, ordenação)."""
    items, total = await list_movies_with_stats(
        session, search, diretor, genero, ano, order_by, order_direction, page, page_size
    )
    pages = (total + page_size - 1) // page_size

    return PaginatedMovies(items=items, total=total, page=page, page_size=page_size, pages=pages)


@router.get("/genres", response_model=GenreList)
async def get_genres(session: AsyncSession = Depends(get_db)) -> GenreList:
    """Retorna lista de todos os gêneros disponíveis."""
    genres = await list_genres(session)
    genre_names = [clean_text(g.nome_genero) for g in genres]
    return GenreList(genres=sorted(set(genre_names)))


def clean_text(value: str | None) -> str | None:
    """Remove escape characters and corrupted encoding from text."""
    if not value:
        return value
    value = value.replace('"""', '"').replace('""', '')
    value = value.strip('"')
    value = value.replace('M-bM-^@M-^S', "'")
    value = value.replace('M-bM-^@M-^Y', '"')
    return value.strip() if value else None


@router.get("/{movie_id}", response_model=MovieDetail)
async def get_movie(movie_id: str, session: AsyncSession = Depends(get_db)) -> MovieDetail:
    """Obtém detalhes de um filme."""
    try:
        return await get_movie_detail(session, movie_id)
    except MovieNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado")


@router.post("", response_model=MovieDetail, status_code=status.HTTP_201_CREATED)
async def create_movie(
    data: MovieCreate, session: AsyncSession = Depends(get_db)
) -> MovieDetail:
    """Cria um novo filme."""
    return await create_movie_service(session, data)


@router.put("/{movie_id}", response_model=MovieDetail)
async def update_movie(
    movie_id: str, data: MovieUpdate, session: AsyncSession = Depends(get_db)
) -> MovieDetail:
    """Atualiza um filme."""
    try:
        return await update_movie_service(session, movie_id, data)
    except MovieNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado")


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: str, session: AsyncSession = Depends(get_db)) -> None:
    """Deleta um filme."""
    try:
        await delete_movie_service(session, movie_id)
    except MovieNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado")


@router.post("/{movie_id}/reviews", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
async def add_review(
    movie_id: str, data: ReviewCreate, session: AsyncSession = Depends(get_db)
) -> ReviewOut:
    """Adiciona uma nova avaliação a um filme."""
    try:
        return await add_review_service(session, movie_id, data)
    except MovieNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Filme não encontrado")
