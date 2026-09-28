import { apiClient } from './client';
import {
  CreateMovieRequest,
  CreateReviewRequest,
  MovieDetail,
  PaginatedMovies,
  UpdateMovieRequest,
} from './types';

export const moviesApi = {
  listMovies: (
    search?: string,
    diretor?: string,
    genero?: string,
    ano?: string,
    orderBy?: string,
    orderDirection?: string,
    page?: number,
    pageSize?: number
  ): Promise<PaginatedMovies> => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (diretor) params.append('diretor', diretor);
    if (genero) params.append('genero', genero);
    if (ano) params.append('ano', ano);
    if (orderBy) params.append('order_by', orderBy);
    if (orderDirection) params.append('order_direction', orderDirection);
    if (page) params.append('page', String(page));
    if (pageSize) params.append('page_size', String(pageSize));

    const query = params.toString() ? `?${params}` : '';
    return apiClient.get(`/movies${query}`);
  },

  getMovie: (movieId: string): Promise<MovieDetail> => {
    return apiClient.get(`/movies/${movieId}`);
  },

  createMovie: (data: CreateMovieRequest): Promise<MovieDetail> => {
    return apiClient.post('/movies', data);
  },

  updateMovie: (movieId: string, data: UpdateMovieRequest): Promise<MovieDetail> => {
    return apiClient.put(`/movies/${movieId}`, data);
  },

  deleteMovie: (movieId: string): Promise<void> => {
    return apiClient.delete(`/movies/${movieId}`);
  },

  addReview: (movieId: string, data: CreateReviewRequest) => {
    return apiClient.post(`/movies/${movieId}/reviews`, data);
  },

  getGenres: (): Promise<{ genres: string[] }> => {
    return apiClient.get('/movies/genres');
  },
};
