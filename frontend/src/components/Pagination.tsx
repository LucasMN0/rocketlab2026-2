import React from 'react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange }) => {
  if (totalPages <= 1) return null;

  // Gera array de números de página a exibir
  const getPageNumbers = () => {
    const pages: (number | string)[] = [];
    const maxVisible = 7; // Máximo de números a exibir
    const sidesCount = 2; // Números antes e depois da página atual

    if (totalPages <= maxVisible) {
      // Mostrar todas as páginas se forem poucas
      for (let i = 1; i <= totalPages; i++) {
        pages.push(i);
      }
    } else {
      // Sempre mostrar primeira página
      pages.push(1);

      // Calcular intervalo ao redor da página atual
      const start = Math.max(2, currentPage - sidesCount);
      const end = Math.min(totalPages - 1, currentPage + sidesCount);

      // Adicionar "..." se houver gap entre 1 e o início do intervalo
      if (start > 2) {
        pages.push('...');
      }

      // Adicionar páginas ao redor da atual
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }

      // Adicionar "..." se houver gap entre o fim do intervalo e a última página
      if (end < totalPages - 1) {
        pages.push('...');
      }

      // Sempre mostrar última página
      pages.push(totalPages);
    }

    return pages;
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="pagination">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="pagination-btn pagination-prev"
        title="Página anterior"
      >
        ← Anterior
      </button>

      <div className="pagination-numbers">
        {pageNumbers.map((page, idx) => (
          <React.Fragment key={idx}>
            {page === '...' ? (
              <span className="pagination-ellipsis">...</span>
            ) : (
              <button
                onClick={() => onPageChange(page as number)}
                className={`pagination-number ${currentPage === page ? 'active' : ''}`}
                disabled={currentPage === page}
                title={`Ir para página ${page}`}
              >
                {page}
              </button>
            )}
          </React.Fragment>
        ))}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="pagination-btn pagination-next"
        title="Próxima página"
      >
        Próxima →
      </button>
    </div>
  );
};
