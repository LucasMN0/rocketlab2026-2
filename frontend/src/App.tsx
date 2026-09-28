import React from 'react';
import { Outlet } from 'react-router-dom';
import './styles/index.css';

export const App: React.FC = () => {
  return (
    <div className="app">
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="app-footer">
        <p>Cinema Review © 2026 - Administrador de Avaliações de Filmes</p>
      </footer>
    </div>
  );
};
