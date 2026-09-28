"""Script para popular o banco de dados com dados dos CSVs."""

import argparse
import csv
import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.movies.models import (
    DimCompany,
    DimGenre,
    DimMovie,
    DimPerson,
    DimReview,
    FactMoviePerformance,
    MovieReview,
)

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

DEFAULT_DATA_DIR_1 = Path("/home/lucas/DESAFIO/cinema/bases-1/bases_atv_dev1")
DEFAULT_DATA_DIR_2 = Path("/home/lucas/DESAFIO/cinema/bases-2/bases_atv_dev_2")


def load_genres(session: Session, csv_path: Path) -> dict[str, DimGenre]:
    """Carrega gêneros do CSV (verificando se já existem)."""
    logger.info(f"Carregando gêneros de {csv_path}")
    genres = {}
    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing = session.query(DimGenre).filter_by(sk_genre_id=row["sk_genre_id"]).first()
            if existing:
                genres[existing.sk_genre_id] = existing
                skipped += 1
            else:
                genre = DimGenre(
                    sk_genre_id=row["sk_genre_id"], nome_genero=row["nome_genero"]
                )
                genres[genre.sk_genre_id] = genre
                session.add(genre)
                inserted += 1

    session.commit()
    logger.info(f"Gêneros: {inserted} inseridos, {skipped} já existiam")
    return genres


def load_companies(session: Session, csv_path: Path) -> dict[str, DimCompany]:
    """Carrega produtoras do CSV (verificando se já existem)."""
    logger.info(f"Carregando produtoras de {csv_path}")
    companies = {}
    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing = session.query(DimCompany).filter_by(sk_company_id=row["sk_company_id"]).first()
            if existing:
                companies[existing.sk_company_id] = existing
                skipped += 1
            else:
                company = DimCompany(
                    sk_company_id=row["sk_company_id"], nome_produtora=row["nome_produtora"]
                )
                companies[company.sk_company_id] = company
                session.add(company)
                inserted += 1

    session.commit()
    logger.info(f"Produtoras: {inserted} inseridas, {skipped} já existiam")
    return companies


def load_people(session: Session, csv_path: Path) -> dict[str, DimPerson]:
    """Carrega pessoas do CSV (verificando se já existem)."""
    logger.info(f"Carregando pessoas de {csv_path}")
    people = {}
    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing = session.query(DimPerson).filter_by(sk_person_id=row["sk_person_id"]).first()
            if existing:
                people[existing.sk_person_id] = existing
                skipped += 1
            else:
                person = DimPerson(
                    sk_person_id=row["sk_person_id"],
                    nome_pessoa=row["nome_pessoa"],
                    tipo_pessoa=row["tipo_pessoa"],
                )
                people[person.sk_person_id] = person
                session.add(person)
                inserted += 1

    session.commit()
    logger.info(f"Pessoas: {inserted} inseridas, {skipped} já existiam")
    return people


def load_movies(session: Session, csv_path: Path) -> dict[str, DimMovie]:
    """Carrega filmes do CSV (verificando se já existem)."""
    logger.info(f"Carregando filmes de {csv_path}")
    movies = {}
    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                existing = session.query(DimMovie).filter_by(sk_movie_id=row["sk_movie_id"]).first()
                if existing:
                    movies[existing.sk_movie_id] = existing
                    skipped += 1
                    continue

                data_lancamento = None
                if row.get("data_lancamento") and row["data_lancamento"].strip():
                    data_lancamento = datetime.strptime(
                        row["data_lancamento"], "%Y-%m-%d"
                    ).date()

                ano_lancamento = None
                if row.get("ano_lancamento") and row["ano_lancamento"].strip():
                    ano_lancamento = int(row["ano_lancamento"])

                duracao = None
                if row.get("duracao_minutos") and row["duracao_minutos"].strip():
                    duracao = int(row["duracao_minutos"])

                movie = DimMovie(
                    sk_movie_id=row["sk_movie_id"],
                    id_filme=row["id_filme"],
                    titulo=row["titulo"],
                    data_lancamento=data_lancamento,
                    ano_lancamento=ano_lancamento,
                    duracao_minutos=duracao,
                    status_filme=row.get("status_filme") or None,
                    sinopse=row.get("sinopse") or None,
                    url_poster=row.get("url_poster") or None,
                    url_backdrop=row.get("url_backdrop") or None,
                )
                movies[movie.sk_movie_id] = movie
                session.add(movie)
                inserted += 1
            except Exception as e:
                logger.error(f"Erro ao processar filme {row.get('sk_movie_id')}: {e}")
                raise

    session.commit()
    logger.info(f"Filmes: {inserted} inseridos, {skipped} já existiam")
    return movies


def load_bridges(
    session: Session,
    csv_path: Path,
    movies: dict[str, DimMovie],
    genres: dict[str, DimGenre],
    companies: dict[str, DimCompany],
    people: dict[str, DimPerson],
) -> None:
    """Carrega tabelas de associação N:N."""
    if csv_path.name == "bridge_movie_genre.csv":
        logger.info(f"Carregando bridge_movie_genre de {csv_path}")
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                movie = movies.get(row["sk_movie_id"])
                genre = genres.get(row["sk_genre_id"])
                if movie and genre and genre not in movie.genres:
                    movie.genres.append(genre)
        logger.info("Bridge movie_genre carregada")

    elif csv_path.name == "bridge_movie_company.csv":
        logger.info(f"Carregando bridge_movie_company de {csv_path}")
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                movie = movies.get(row["sk_movie_id"])
                company = companies.get(row["sk_company_id"])
                if movie and company and company not in movie.companies:
                    movie.companies.append(company)
        logger.info("Bridge movie_company carregada")

    elif csv_path.name == "bridge_movie_person.csv":
        logger.info(f"Carregando bridge_movie_person de {csv_path}")
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                movie = movies.get(row["sk_movie_id"])
                person = people.get(row["sk_person_id"])
                if movie and person and person not in movie.people:
                    movie.people.append(person)
        logger.info("Bridge movie_person carregada")

    session.commit()


def load_performance(
    session: Session, csv_path: Path, movies: dict[str, DimMovie]
) -> None:
    """Carrega dados de desempenho financeiro (verificando se já existem)."""
    logger.info(f"Carregando performance de {csv_path}")
    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["sk_movie_id"] not in movies:
                continue

            existing = session.query(FactMoviePerformance).filter_by(sk_movie_id=row["sk_movie_id"]).first()
            if existing:
                skipped += 1
                continue

            try:
                performance = FactMoviePerformance(
                    sk_movie_id=row["sk_movie_id"],
                    orcamento_usd=float(row["orcamento_usd"])
                    if row.get("orcamento_usd") and row["orcamento_usd"].strip()
                    else None,
                    receita_usd=float(row["receita_usd"])
                    if row.get("receita_usd") and row["receita_usd"].strip()
                    else None,
                    lucro_usd=float(row["lucro_usd"])
                    if row.get("lucro_usd") and row["lucro_usd"].strip()
                    else 0.0,
                    orcamento_brl=float(row["orcamento_brl"])
                    if row.get("orcamento_brl") and row["orcamento_brl"].strip()
                    else None,
                    receita_brl=float(row["receita_brl"])
                    if row.get("receita_brl") and row["receita_brl"].strip()
                    else None,
                    lucro_brl=float(row["lucro_brl"])
                    if row.get("lucro_brl") and row["lucro_brl"].strip()
                    else 0.0,
                    popularidade=float(row["popularidade"])
                    if row.get("popularidade") and row["popularidade"].strip()
                    else None,
                    nota_tmdb=float(row["nota_tmdb"])
                    if row.get("nota_tmdb") and row["nota_tmdb"].strip()
                    else None,
                    qtd_tmdb=int(float(row["qtd_tmdb"]))
                    if row.get("qtd_tmdb") and row["qtd_tmdb"].strip()
                    else None,
                    nota_imdb=float(row["nota_imdb"])
                    if row.get("nota_imdb") and row["nota_imdb"].strip()
                    else None,
                    qtd_imdb=int(float(row["qtd_imdb"]))
                    if row.get("qtd_imdb") and row["qtd_imdb"].strip()
                    else None,
                )
                session.add(performance)
                inserted += 1
            except Exception as e:
                logger.error(f"Erro ao processar performance {row.get('sk_movie_id')}: {e}")
                raise

    session.commit()
    logger.info(f"Performance: {inserted} inseridas, {skipped} já existiam")


def load_reviews(session: Session, csv_path: Path) -> None:
    """Carrega avaliações individuais de filmes (verificando se já existem)."""
    logger.info(f"Carregando avaliações de {csv_path}")
    inserted = 0
    skipped = 0

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing = session.query(MovieReview).filter_by(sk_movie_review_id=row["sk_movie_review_id"]).first()
            if existing:
                skipped += 1
                continue

            try:
                review = MovieReview(
                    sk_movie_review_id=row["sk_movie_review_id"],
                    sk_movie_id=row["sk_movie_id"],
                    nome=row["nome"],
                    nota=float(row["nota"]),
                    comentario=row["comentario"],
                )
                session.add(review)
                inserted += 1
            except Exception as e:
                logger.error(f"Erro ao processar review {row.get('sk_movie_review_id')}: {e}")
                raise

    session.commit()
    logger.info(f"Avaliações: {inserted} inseridas, {skipped} já existiam")


def recalculate_review_summaries(session: Session) -> None:
    """Recalcula resumos de avaliações (DimReview) a partir das reviews."""
    logger.info("Recalculando resumos de avaliações...")

    movies = session.query(DimMovie).order_by(DimMovie.sk_movie_id).all()

    for movie in movies:
        result = session.query(
            func.avg(MovieReview.nota), func.count(MovieReview.sk_movie_review_id)
        ).filter(MovieReview.sk_movie_id == movie.sk_movie_id).one()

        avg_nota, count = result

        review_summary = DimReview(
            sk_movie_id=movie.sk_movie_id,
            qtd_avaliacoes_usuarios=count or 0,
            nota_media_usuarios=float(avg_nota) if avg_nota else None,
        )
        session.add(review_summary)

    session.commit()
    logger.info(f"Recalculados resumos para {len(movies)} filmes")


def main(data_dir_1: Path, data_dir_2: Path) -> None:
    """Orquestra o carregamento de todos os dados."""
    db_url = settings.database_url
    if db_url.startswith("sqlite+aiosqlite"):
        db_url = db_url.replace("sqlite+aiosqlite", "sqlite")

    engine = create_engine(db_url, echo=False)

    with Session(engine) as session:
        # Ordem de carga respeita constraints de FK
        logger.info("Iniciando carga de dados...")

        genres = load_genres(session, data_dir_1 / "dim_genres.csv")
        companies = load_companies(session, data_dir_1 / "dim_companies.csv")
        people = load_people(session, data_dir_1 / "dim_people.csv")
        movies = load_movies(session, data_dir_1 / "dim_movies.csv")

        # Carrega bridges
        load_bridges(
            session, data_dir_2 / "bridge_movie_genre.csv", movies, genres, companies, people
        )
        load_bridges(
            session, data_dir_2 / "bridge_movie_company.csv", movies, genres, companies, people
        )
        load_bridges(
            session, data_dir_2 / "bridge_movie_person.csv", movies, genres, companies, people
        )

        # Carrega performance e reviews
        load_performance(session, data_dir_2 / "fact_movies_performance.csv", movies)
        load_reviews(session, data_dir_2 / "movies_reviews.csv")

        # Recalcula resumos de avaliações
        recalculate_review_summaries(session)

        logger.info("Carga de dados concluída com sucesso!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Popula o banco com dados dos CSVs")
    parser.add_argument(
        "--data-dir-1",
        type=Path,
        default=DEFAULT_DATA_DIR_1,
        help=f"Diretório com CSVs de dimensões (default: {DEFAULT_DATA_DIR_1})",
    )
    parser.add_argument(
        "--data-dir-2",
        type=Path,
        default=DEFAULT_DATA_DIR_2,
        help=f"Diretório com CSVs de fatos e bridges (default: {DEFAULT_DATA_DIR_2})",
    )

    args = parser.parse_args()

    if not args.data_dir_1.exists():
        logger.error(f"Diretório não encontrado: {args.data_dir_1}")
        exit(1)

    if not args.data_dir_2.exists():
        logger.error(f"Diretório não encontrado: {args.data_dir_2}")
        exit(1)

    main(args.data_dir_1, args.data_dir_2)
