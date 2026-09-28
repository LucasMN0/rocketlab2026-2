"""Fixtures compartilhadas pelos testes da API de filmes.

Cada teste recebe um banco SQLite novo em um diretório temporário,
então os testes nunca tocam o banco real e não dependem uns dos outros.
"""

from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

# AJUSTE: importe o módulo onde estão DimMovie, DimGenre etc.
# O import é necessário para registrar as tabelas no Base.metadata.
import app.movies.models  # noqa: F401
from app.db.base import Base
from app.db.session import enable_sqlite_foreign_keys, get_db
from app.main import app


@pytest_asyncio.fixture
async def session_factory(tmp_path) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """Cria um banco SQLite descartável com todas as tabelas."""

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{tmp_path / 'test.db'}",
        poolclass=NullPool,
    )
    enable_sqlite_foreign_keys(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    factory = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    yield factory

    await engine.dispose()


@pytest_asyncio.fixture
async def client(session_factory) -> AsyncIterator[AsyncClient]:
    """Cliente HTTP que usa o banco de teste no lugar do banco real."""

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()