import React, { useState } from 'react';
import { CreateReviewRequest } from '../api/types';

interface ReviewFormProps {
  onSubmit: (data: CreateReviewRequest) => Promise<void>;
  isLoading?: boolean;
}

export const ReviewForm: React.FC<ReviewFormProps> = ({ onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState<CreateReviewRequest>({
    nome: '',
    nota: 5,
    comentario: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'nota' ? parseFloat(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.nome.trim() || !formData.comentario.trim()) {
      setError('Nome e comentário são obrigatórios');
      return;
    }

    if (formData.nota < 0 || formData.nota > 10) {
      setError('Nota deve estar entre 0 e 10');
      return;
    }

    try {
      await onSubmit(formData);
      setFormData({ nome: '', nota: 5, comentario: '' });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao adicionar avaliação');
    }
  };

  return (
    <form className="review-form" onSubmit={handleSubmit}>
      <h3>Adicionar Avaliação</h3>
      {error && <div className="error-message">{error}</div>}

      <input
        type="text"
        name="nome"
        placeholder="Seu nome"
        value={formData.nome}
        onChange={handleChange}
        disabled={isLoading}
        required
      />

      <div className="form-row">
        <div className="form-group">
          <label>Nota (0-10)</label>
          <input
            type="number"
            name="nota"
            min="0"
            max="10"
            step="0.1"
            value={formData.nota}
            onChange={handleChange}
            disabled={isLoading}
            required
          />
        </div>
      </div>

      <textarea
        name="comentario"
        placeholder="Sua resenha..."
        value={formData.comentario}
        onChange={handleChange}
        disabled={isLoading}
        rows={4}
        required
      />

      <button type="submit" disabled={isLoading} className="submit-btn">
        {isLoading ? 'Enviando...' : 'Enviar Avaliação'}
      </button>
    </form>
  );
};
