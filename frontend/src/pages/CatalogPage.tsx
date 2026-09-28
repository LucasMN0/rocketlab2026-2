import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { moviesApi } from '../api/movies';
import { MovieListItem } from '../api/types';
import { MovieCard } from '../components/MovieCard';
import { SearchBar } from '../components/SearchBar';
import { Pagination } from '../components/Pagination';

export const CatalogPage: React.FC = () => {
  const navigate = useNavigate();
  const [movies, setMovies] = useState<MovieListItem[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const PAGE_SIZE = 10;

  useEffect(() => {
    loadMovies();
  }, [currentPage, searchQuery]);

  const loadMovies = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await moviesApi.listMovies(searchQuery, currentPage, PAGE_SIZE);
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

  return (
    <div className="catalog-page">
      <header className="catalog-header">
        <h1>Cinema - Catálogo</h1>
        <button onClick={() => navigate('/movies/new')} className="btn-primary">
          + Novo Filme
        </button>
      </header>

      <SearchBar onSearch={handleSearch} />

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
