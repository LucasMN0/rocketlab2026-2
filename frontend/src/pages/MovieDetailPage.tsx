import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { moviesApi } from '../api/movies';
import { MovieDetail, CreateReviewRequest } from '../api/types';
import { ReviewForm } from '../components/ReviewForm';
import { ReviewList } from '../components/ReviewList';
import { StarRating } from '../components/StarRating';
import { ConfirmDialog } from '../components/ConfirmDialog';

export const MovieDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [movie, setMovie] = useState<MovieDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [reviewLoading, setReviewLoading] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

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

  const handleAddReview = async (data: CreateReviewRequest) => {
    if (!id) return;
    try {
      setReviewLoading(true);
      setError('');
      await moviesApi.addReview(id, data);
      await loadMovie();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao adicionar avaliação');
      throw err;
    } finally {
      setReviewLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!id) return;
    try {
      setDeleting(true);
      await moviesApi.deleteMovie(id);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao deletar filme');
      setDeleteConfirm(false);
      setDeleting(false);
    }
  };

  if (loading) {
    return <div className="loading">Carregando...</div>;
  }

  if (!movie) {
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
    <div className="movie-detail-page">
      <button onClick={() => navigate('/')} className="btn-back">
        ← Voltar
      </button>

      {error && <div className="error-message">{error}</div>}

      <div className="movie-hero">
        {movie.url_poster && (
          <img src={movie.url_poster} alt={movie.titulo} className="poster" />
        )}
        <div className="movie-info">
          <h1>{movie.titulo}</h1>
          <p className="director">
            <strong>Diretor:</strong> {movie.diretor}
          </p>
          <p className="year">
            <strong>Ano:</strong> {movie.ano_lancamento}
          </p>
          {movie.genero && (
            <p className="genre">
              <strong>Gênero:</strong> {movie.genero}
            </p>
          )}
          {movie.duracao_minutos && (
            <p className="duration">
              <strong>Duração:</strong> {movie.duracao_minutos} minutos
            </p>
          )}

          <div className="rating-section">
            <div className="rating-info">
              <span className="rating-text">Avaliação média</span>
              <StarRating nota={movie.nota_media} readOnly />
              {movie.nota_media && (
                <span className="rating-value">
                  {movie.nota_media.toFixed(1)}/10
                </span>
              )}
            </div>
            {movie.qtd_avaliacoes > 0 && (
              <p className="avaliacoes-count">{movie.qtd_avaliacoes} avaliações</p>
            )}
          </div>

          <div className="movie-actions">
            <button onClick={() => navigate(`/movies/${id}/edit`)} className="btn-secondary">
              ✏️ Editar
            </button>
            <button onClick={() => setDeleteConfirm(true)} className="btn-danger">
              🗑️ Deletar
            </button>
          </div>
        </div>
      </div>

      {movie.sinopse && (
        <div className="synopsis-section">
          <h2>Sinopse</h2>
          <p>{movie.sinopse}</p>
        </div>
      )}

      <div className="reviews-section">
        <h2>Avaliações</h2>
        <ReviewForm onSubmit={handleAddReview} isLoading={reviewLoading} />
        <ReviewList reviews={movie.reviews || []} />
      </div>

      <ConfirmDialog
        isOpen={deleteConfirm}
        title="Deletar Filme"
        message={`Tem certeza que deseja deletar "${movie.titulo}"? Esta ação não pode ser desfeita.`}
        confirmText="Deletar"
        cancelText="Cancelar"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm(false)}
        isLoading={deleting}
      />
    </div>
  );
};
