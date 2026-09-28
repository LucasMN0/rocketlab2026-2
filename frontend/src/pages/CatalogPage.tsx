import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { moviesApi } from '../api/movies';
import { MovieListItem } from '../api/types';
import { MovieCard } from '../components/MovieCard';
import { SearchBar } from '../components/SearchBar';
import { FilterBar } from '../components/FilterBar';
import { Pagination } from '../components/Pagination';

export const CatalogPage: React.FC = () => {
  const navigate = useNavigate();
  const [movies, setMovies] = useState<MovieListItem[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [diretorFilter, setDiretorFilter] = useState('');
  const [generoFilter, setGeneroFilter] = useState('');
  const [anoFilter, setAnoFilter] = useState('');
  const [orderBy, setOrderBy] = useState('titulo');
  const [orderDirection, setOrderDirection] = useState('asc');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const PAGE_SIZE = 10;

  useEffect(() => {
    loadMovies();
  }, [currentPage, searchQuery, diretorFilter, generoFilter, anoFilter, orderBy, orderDirection]);

  const loadMovies = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await moviesApi.listMovies(
        searchQuery,
        diretorFilter,
        generoFilter,
        anoFilter,
        orderBy,
        orderDirection,
        currentPage,
        PAGE_SIZE
      );
      setMovies(data.items);
      setTotalPages(Math.ceil(data.total / PAGE_SIZE));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar filmes');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1);
  };

  const handleFilter = (diretor: string, genero: string) => {
    setDiretorFilter(diretor);
    setGeneroFilter(genero);
    setCurrentPage(1);
  };

  return (
    <div className="catalog-page">
      <header className="catalog-header">
        <div className="header-left">
          <h1>Cinema - Catálogo</h1>
        </div>
        <div className="header-right">
          <button onClick={() => navigate('/movies/new')} className="btn-primary">
            + Novo Filme
          </button>
        </div>
      </header>

      <div className="sort-bar">
        <div className="sort-group">
          <label htmlFor="order-by">Ordenar por:</label>
          <select
            id="order-by"
            value={orderBy}
            onChange={(e) => {
              setOrderBy(e.target.value);
              setCurrentPage(1);
            }}
            className="sort-select"
          >
            <option value="titulo">Título</option>
            <option value="ano_lancamento">Ano</option>
            <option value="nota_media">Avaliação</option>
          </select>
        </div>

        <div className="sort-group">
          <label htmlFor="order-direction">Ordem:</label>
          <select
            id="order-direction"
            value={orderDirection}
            onChange={(e) => {
              setOrderDirection(e.target.value);
              setCurrentPage(1);
            }}
            className="sort-select"
          >
            <option value="asc">Crescente (↑)</option>
            <option value="desc">Decrescente (↓)</option>
          </select>
        </div>

        <div className="sort-group">
          <label htmlFor="ano-filter">Ano:</label>
          <input
            id="ano-filter"
            type="number"
            min="1900"
            max={new Date().getFullYear()}
            placeholder="Filtrar por ano"
            value={anoFilter}
            onChange={(e) => {
              setAnoFilter(e.target.value);
              setCurrentPage(1);
            }}
            className="sort-input"
          />
          {anoFilter && (
            <button
              onClick={() => {
                setAnoFilter('');
                setCurrentPage(1);
              }}
              className="sort-clear"
              title="Limpar filtro de ano"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      <div className="controls-section">
        <SearchBar onSearch={handleSearch} />
        <FilterBar onSearch={handleFilter} isLoading={loading} />
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Carregando...</div>
      ) : movies.length === 0 ? (
        <div className="no-results">
          {searchQuery
            ? 'Nenhum filme encontrado com essa busca'
            : 'Nenhum filme no catálogo ainda'}
        </div>
      ) : (
        <>
          <div className="movies-grid">
            {movies.map((movie) => (
              <MovieCard
                key={movie.id_filme}
                movie={movie}
                onViewDetails={() => navigate(`/movies/${movie.id_filme}`)}
              />
            ))}
          </div>
          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPageChange={setCurrentPage}
          />
        </>
      )}
    </div>
  );
};
