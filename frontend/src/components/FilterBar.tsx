import React, { useState, useEffect } from 'react';
import { moviesApi } from '../api/movies';

interface FilterBarProps {
  onSearch: (diretor: string, genero: string) => void;
  isLoading?: boolean;
}

export const FilterBar: React.FC<FilterBarProps> = ({ onSearch, isLoading = false }) => {
  const [diretor, setDiretor] = useState('');
  const [genero, setGenero] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [generos, setGeneros] = useState<string[]>([]);
  const [loadingGeneros, setLoadingGeneros] = useState(false);

  useEffect(() => {
    loadGeneros();
  }, []);

  const loadGeneros = async () => {
    try {
      setLoadingGeneros(true);
      const data = await moviesApi.getGenres();
      setGeneros(data.genres);
    } catch (err) {
      console.error('Erro ao carregar gêneros:', err);
    } finally {
      setLoadingGeneros(false);
    }
  };

  const handleFilter = () => {
    onSearch(diretor, genero);
  };

  const handleClear = () => {
    setDiretor('');
    setGenero('');
    onSearch('', '');
  };

  const hasFilters = diretor.trim() || genero.trim();

  return (
    <div className="filter-bar">
      <button
        className="filter-toggle"
        onClick={() => setIsOpen(!isOpen)}
        title="Abrir filtros avançados"
      >
        ⚙️ Filtros {hasFilters && <span className="filter-badge">2</span>}
      </button>

      {isOpen && (
        <div className="filter-panel">
          <div className="filter-group">
            <label htmlFor="diretor">🎬 Diretor</label>
            <input
              id="diretor"
              type="text"
              placeholder="Ex: Steven Spielberg"
              value={diretor}
              onChange={(e) => setDiretor(e.target.value)}
              disabled={isLoading}
              autoComplete="off"
            />
          </div>

          <div className="filter-group">
            <label htmlFor="genero">🎭 Gênero</label>
            {loadingGeneros ? (
              <div className="loading-genres">Carregando gêneros...</div>
            ) : (
              <select
                id="genero"
                value={genero}
                onChange={(e) => setGenero(e.target.value)}
                disabled={isLoading || loadingGeneros}
                className="genre-select"
              >
                <option value="">-- Selecione um gênero --</option>
                {generos.map((g) => (
                  <option key={g} value={g}>
                    {g}
                  </option>
                ))}
              </select>
            )}
          </div>

          <div className="filter-actions">
            <button onClick={handleFilter} disabled={isLoading} className="filter-btn">
              {isLoading ? '⏳ Filtrando...' : '✨ Filtrar'}
            </button>
            {hasFilters && (
              <button onClick={handleClear} disabled={isLoading} className="filter-clear-btn">
                ✕ Limpar
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
