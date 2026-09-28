import React from 'react';
import { createBrowserRouter, RouteObject } from 'react-router-dom';
import { App } from './App';
import { CatalogPage } from './pages/CatalogPage';
import { MovieDetailPage } from './pages/MovieDetailPage';
import { MovieFormPage } from './pages/MovieFormPage';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <CatalogPage />,
      },
      {
        path: 'movies/new',
        element: <MovieFormPage />,
      },
      {
        path: 'movies/:id/edit',
        element: <MovieFormPage />,
      },
      {
        path: 'movies/:id',
        element: <MovieDetailPage />,
      },
    ],
  },
];

export const router = createBrowserRouter(routes);
