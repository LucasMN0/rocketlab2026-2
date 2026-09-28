import React from 'react';
import { Review } from '../api/types';

interface ReviewListProps {
  reviews: Review[];
}

export const ReviewList: React.FC<ReviewListProps> = ({ reviews }) => {
  if (reviews.length === 0) {
    return <p className="no-reviews">Nenhuma avaliação ainda</p>;
  }

  return (
    <div className="review-list">
      {reviews.map((review) => (
        <div key={review.sk_movie_review_id} className="review-item">
          <div className="review-header">
            <span className="review-name">{review.nome}</span>
            <span className="review-note">{review.nota}/10 ⭐</span>
          </div>
          <p className="review-comment">{review.comentario}</p>
          <span className="review-date">
            {new Date(review.created_at).toLocaleDateString('pt-BR')}
          </span>
        </div>
      ))}
    </div>
  );
};
