export interface Movie {
  sk_movie_id: string;
  id_filme: string;
  titulo: string;
  ano_lancamento: number | null;
  duracao_minutos: number | null;
  sinopse: string | null;
  genero: string | null;
  diretor: string | null;
  url_poster: string | null;
  url_backdrop: string | null;
  nota_media: number | null;
  qtd_avaliacoes: number;
}

export interface MovieDetail extends Movie {
  reviews: Review[];
}

export interface MovieListItem {
  sk_movie_id: string;
  titulo: string;
  ano_lancamento: number | null;
  genero: string | null;
  diretor: string | null;
  url_poster: string | null;
  nota_media: number | null;
  qtd_avaliacoes: number;
}

export interface Review {
  sk_movie_review_id: string;
  nome: string;
  nota: number;
  comentario: string;
  created_at: string;
}

export interface PaginatedMovies {
  items: MovieListItem[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

export interface CreateMovieRequest {
  titulo: string;
  diretor: string;
  ano_lancamento: number;
  genero: string;
  sinopse?: string;
  duracao_minutos?: number;
  url_poster?: string;
}

export interface UpdateMovieRequest {
  titulo?: string;
  diretor?: string;
  ano_lancamento?: number;
  genero?: string;
  sinopse?: string;
  duracao_minutos?: number;
  url_poster?: string;
}

export interface CreateReviewRequest {
  nome: string;
  nota: number;
  comentario: string;
}
