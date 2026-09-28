import React from 'react';

interface StarRatingProps {
  nota: number | null;
  readOnly?: boolean;
  onChange?: (nota: number) => void;
}

export const StarRating: React.FC<StarRatingProps> = ({ nota, readOnly = true, onChange }) => {
  const convertToStars = (notaDezescala: number | null) => {
    if (notaDezescala === null) return 0;
    return notaDezescala / 2;
  };

  const stars = convertToStars(nota);
  const maxStars = 5;

  return (
    <div className="star-rating">
      {Array.from({ length: maxStars }).map((_, i) => {
        const fillPercentage = Math.min(Math.max(stars - i, 0), 1);
        return (
          <span
            key={i}
            className={`star ${fillPercentage >= 0.5 ? 'filled' : fillPercentage > 0 ? 'half' : 'empty'}`}
            onClick={() => !readOnly && onChange?.(Math.round((i + 1) * 2 * 10) / 10)}
            style={{ cursor: readOnly ? 'default' : 'pointer' }}
          >
            ★
          </span>
        );
      })}
      {nota !== null && <span className="nota-text">{nota.toFixed(1)}/10</span>}
    </div>
  );
};
