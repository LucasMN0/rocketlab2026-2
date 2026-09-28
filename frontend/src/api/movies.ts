import { apiClient } from './client';
import {
  CreateMovieRequest,
  CreateReviewRequest,
  MovieDetail,
  PaginatedMovies,
  UpdateMovieRequest,
} from './types';

export const moviesApi = {
  listMovies: (search?: string, page?: number, pageSize?: number): Promise<PaginatedMovies> => {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
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
};
