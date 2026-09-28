"""Add performance indexes for search and filtering.

Revision ID: 0002_add_performance_indexes
Revises: 0001_initial_movie_schema
Create Date: 2026-09-28 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_add_performance_indexes'
down_revision = '0001_initial_movie_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Index para busca por título
    op.create_index('ix_dim_movies_titulo', 'dim_movies', ['titulo'], unique=False)

    # Index para busca por id_filme
    op.create_index('ix_dim_movies_id_filme', 'dim_movies', ['id_filme'], unique=False)

    # Index para busca por diretor
    op.create_index('ix_dim_people_nome_tipo', 'dim_people', ['nome_pessoa', 'tipo_pessoa'], unique=False)

    # Index para busca por gênero
    op.create_index('ix_dim_genres_nome', 'dim_genres', ['nome_genero'], unique=False)

    # Index para filtragem de reviews por filme
    op.create_index('ix_movie_reviews_movie_id', 'movie_reviews', ['sk_movie_id'], unique=False)

    # Index para filtragem de reviews por nota
    op.create_index('ix_movie_reviews_nota', 'movie_reviews', ['nota'], unique=False)

    # Index para bridge movie-genre
    op.create_index('ix_bridge_movie_genre_movie', 'bridge_movie_genre', ['sk_movie_id'], unique=False)
    op.create_index('ix_bridge_movie_genre_genre', 'bridge_movie_genre', ['sk_genre_id'], unique=False)

    # Index para bridge movie-person
    op.create_index('ix_bridge_movie_person_movie', 'bridge_movie_person', ['sk_movie_id'], unique=False)
    op.create_index('ix_bridge_movie_person_person', 'bridge_movie_person', ['sk_person_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_dim_movies_titulo', table_name='dim_movies')
    op.drop_index('ix_dim_movies_id_filme', table_name='dim_movies')
    op.drop_index('ix_dim_people_nome_tipo', table_name='dim_people')
    op.drop_index('ix_dim_genres_nome', table_name='dim_genres')
    op.drop_index('ix_movie_reviews_movie_id', table_name='movie_reviews')
    op.drop_index('ix_movie_reviews_nota', table_name='movie_reviews')
    op.drop_index('ix_bridge_movie_genre_movie', table_name='bridge_movie_genre')
    op.drop_index('ix_bridge_movie_genre_genre', table_name='bridge_movie_genre')
    op.drop_index('ix_bridge_movie_person_movie', table_name='bridge_movie_person')
    op.drop_index('ix_bridge_movie_person_person', table_name='bridge_movie_person')
