import React, { useState, useEffect } from 'react';
import { CreateMovieRequest, UpdateMovieRequest, MovieDetail } from '../api/types';

interface MovieFormProps {
  initialMovie?: MovieDetail;
  onSubmit: (data: CreateMovieRequest | UpdateMovieRequest) => Promise<void>;
  isLoading?: boolean;
}

export const MovieForm: React.FC<MovieFormProps> = ({ initialMovie, onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState({
    titulo: '',
    diretor: '',
    ano_lancamento: new Date().getFullYear(),
    genero: '',
    sinopse: '',
    duracao_minutos: '',
    url_poster: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialMovie) {
      setFormData({
        titulo: initialMovie.titulo,
        diretor: initialMovie.diretor || '',
        ano_lancamento: initialMovie.ano_lancamento || new Date().getFullYear(),
        genero: initialMovie.genero || '',
        sinopse: initialMovie.sinopse || '',
        duracao_minutos: initialMovie.duracao_minutos?.toString() || '',
        url_poster: initialMovie.url_poster || '',
      });
    }
  }, [initialMovie]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'ano_lancamento' || name === 'duracao_minutos' ? value : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.titulo.trim() || !formData.diretor.trim() || !formData.genero.trim()) {
      setError('Título, diretor e gênero são obrigatórios');
      return;
    }

    try {
      const data = {
        titulo: formData.titulo,
        diretor: formData.diretor,
        ano_lancamento: parseInt(formData.ano_lancamento as any) || new Date().getFullYear(),
        genero: formData.genero,
        ...(formData.sinopse && { sinopse: formData.sinopse }),
        ...(formData.duracao_minutos && { duracao_minutos: parseInt(formData.duracao_minutos) }),
        ...(formData.url_poster && { url_poster: formData.url_poster }),
      };

      await onSubmit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao salvar filme');
    }
  };

  return (
    <form className="movie-form" onSubmit={handleSubmit}>
      <h2>{initialMovie ? 'Editar Filme' : 'Novo Filme'}</h2>
      {error && <div className="error-message">{error}</div>}

      <input
        type="text"
        name="titulo"
        placeholder="Título"
        value={formData.titulo}
        onChange={handleChange}
        disabled={isLoading}
        required
      />

      <input
        type="text"
        name="diretor"
        placeholder="Diretor"
        value={formData.diretor}
        onChange={handleChange}
        disabled={isLoading}
        required
      />

      <div className="form-row">
        <input
          type="number"
          name="ano_lancamento"
          placeholder="Ano"
          value={formData.ano_lancamento}
          onChange={handleChange}
          disabled={isLoading}
        />
        <input
          type="number"
          name="duracao_minutos"
          placeholder="Duração (min)"
          value={formData.duracao_minutos}
          onChange={handleChange}
          disabled={isLoading}
        />
      </div>

      <input
        type="text"
        name="genero"
        placeholder="Gênero"
        value={formData.genero}
        onChange={handleChange}
        disabled={isLoading}
        required
      />

      <textarea
        name="sinopse"
        placeholder="Sinopse"
        value={formData.sinopse}
        onChange={handleChange}
        disabled={isLoading}
        rows={3}
      />

      <input
        type="url"
        name="url_poster"
        placeholder="URL do Poster"
        value={formData.url_poster}
        onChange={handleChange}
        disabled={isLoading}
      />

      <button type="submit" disabled={isLoading} className="submit-btn">
        {isLoading ? 'Salvando...' : initialMovie ? 'Atualizar' : 'Criar Filme'}
      </button>
    </form>
  );
};
