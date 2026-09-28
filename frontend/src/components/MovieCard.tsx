import React from 'react';
import { Link } from 'react-router-dom';
import { MovieListItem } from '../api/types';
import { StarRating } from './StarRating';

interface MovieCardProps {
  movie: MovieListItem;
}

export const MovieCard: React.FC<MovieCardProps> = ({ movie }) => {
  return (
    <Link to={`/movies/${movie.id_filme}`} className="movie-card">
      {movie.url_poster && (
        <img src={movie.url_poster} alt={movie.titulo} className="movie-poster" />
      )}
      <div className="movie-info">
        <h3>{movie.titulo}</h3>
        <p className="year">{movie.ano_lancamento}</p>
        {movie.genero && <p className="genre">{movie.genero}</p>}
        {movie.diretor && <p className="director">{movie.diretor}</p>}
        <div className="rating">
          <StarRating nota={movie.nota_media} />
          <span className="count">({movie.qtd_avaliacoes})</span>
        </div>
      </div>
    </Link>
  );
};
