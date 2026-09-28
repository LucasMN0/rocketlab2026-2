import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { moviesApi } from '../api/movies';
import { CreateMovieRequest, UpdateMovieRequest, MovieDetail } from '../api/types';
import { MovieForm } from '../components/MovieForm';

export const MovieFormPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<MovieDetail | null>(null);
  const [loading, setLoading] = useState(!!id);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadMovie();
    }
  }, [id]);

  const loadMovie = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await moviesApi.getMovie(id!);
      setMovie(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao carregar filme');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (data: CreateMovieRequest | UpdateMovieRequest) => {
    try {
      setSubmitting(true);
      setError('');

      if (id && movie) {
        await moviesApi.updateMovie(id, data as UpdateMovieRequest);
        navigate(`/movies/${id}`);
      } else {
        const newMovie = await moviesApi.createMovie(data as CreateMovieRequest);
        navigate(`/movies/${newMovie.id_filme}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao salvar filme');
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="loading">Carregando...</div>;
  }

  if (id && !movie) {
    return (
      <div className="error-page">
        <h1>Filme não encontrado</h1>
        <button onClick={() => navigate('/')} className="btn-primary">
          Voltar ao Catálogo
        </button>
      </div>
    );
  }

  return (
    <div className="movie-form-page">
      <button onClick={() => navigate(-1)} className="btn-back">
        ← Voltar
      </button>

      {error && <div className="error-message">{error}</div>}

      <MovieForm initialMovie={movie || undefined} onSubmit={handleSubmit} isLoading={submitting} />
    </div>
  );
};
