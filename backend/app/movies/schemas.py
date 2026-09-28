"""Pydantic schemas para requests/responses da API de filmes."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


def clean_text(value: str | None) -> str | None:
    """Remove escape characters and corrupted encoding from text."""
    if not value:
        return value
    # Remove escaped quotes that appear in titles
    value = value.replace('"""', '"').replace('""', '')
    # Remove leading/trailing double quotes
    value = value.strip('"')
    # Clean up common encoding issues
    value = value.replace('M-bM-^@M-^S', "'")  # UTF-8 encoding issue for apostrophe
    value = value.replace('M-bM-^@M-^Y', '"')  # UTF-8 encoding issue for quote
    return value.strip() if value else None


class GenreOut(BaseModel):
    sk_genre_id: str
    nome_genero: str

    @field_validator("nome_genero", mode="before")
    @classmethod
    def clean_fields(cls, v: str | None) -> str | None:
        return clean_text(v)


class PersonOut(BaseModel):
    sk_person_id: str
    nome_pessoa: str
    tipo_pessoa: str

    @field_validator("nome_pessoa", "tipo_pessoa", mode="before")
    @classmethod
    def clean_fields(cls, v: str | None) -> str | None:
        return clean_text(v)


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

    @field_validator("nome", "comentario", mode="before")
    @classmethod
    def clean_fields(cls, v: str | None) -> str | None:
        return clean_text(v)


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
    id_filme: str
    titulo: str
    ano_lancamento: int | None
    genero: str | None
    diretor: str | None
    url_poster: str | None
    nota_media: float | None
    qtd_avaliacoes: int

    @field_validator("titulo", "genero", "diretor", "url_poster", mode="before")
    @classmethod
    def clean_fields(cls, v: str | None) -> str | None:
        return clean_text(v)


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

    @field_validator(
        "titulo", "sinopse", "genero", "diretor", "url_poster", "url_backdrop", mode="before"
    )
    @classmethod
    def clean_fields(cls, v: str | None) -> str | None:
        return clean_text(v)


class PaginatedMovies(BaseModel):
    items: list[MovieListItem]
    total: int
    page: int
    page_size: int
    pages: int


class GenreList(BaseModel):
    genres: list[str]
