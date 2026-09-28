"""Pydantic schemas para requests/responses da API de filmes."""

from datetime import datetime

from pydantic import BaseModel, Field


class GenreOut(BaseModel):
    sk_genre_id: str
    nome_genero: str


class PersonOut(BaseModel):
    sk_person_id: str
    nome_pessoa: str
    tipo_pessoa: str


class ReviewCreate(BaseModel):
    nome: str
    nota: float = Field(ge=0, le=10, description="Nota de 0 a 10")
    comentario: str


class ReviewOut(BaseModel):
    sk_movie_review_id: str
    nome: str
    nota: float
    comentario: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MovieCreate(BaseModel):
    titulo: str
    diretor: str
    ano_lancamento: int
    genero: str
    sinopse: str | None = None
    duracao_minutos: int | None = None
    url_poster: str | None = None


class MovieUpdate(BaseModel):
    titulo: str | None = None
    diretor: str | None = None
    ano_lancamento: int | None = None
    genero: str | None = None
    sinopse: str | None = None
    duracao_minutos: int | None = None
    url_poster: str | None = None


class MovieListItem(BaseModel):
    sk_movie_id: str
    titulo: str
    ano_lancamento: int | None
    genero: str | None
    diretor: str | None
    url_poster: str | None
    nota_media: float | None
    qtd_avaliacoes: int


class MovieDetail(BaseModel):
    sk_movie_id: str
    titulo: str
    ano_lancamento: int | None
    duracao_minutos: int | None
    sinopse: str | None
    genero: str | None
    diretor: str | None
    url_poster: str | None
    url_backdrop: str | None
    nota_media: float | None
    qtd_avaliacoes: int
    reviews: list[ReviewOut]

    model_config = {"from_attributes": True}


class PaginatedMovies(BaseModel):
    items: list[MovieListItem]
    total: int
    page: int
    page_size: int
    pages: int
