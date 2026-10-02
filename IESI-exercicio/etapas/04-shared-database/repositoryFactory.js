import { CsvProdutoRepository } from './CsvProdutoRepository.js';
import { SqliteProdutoRepository } from './SqliteProdutoRepository.js';

// Simple Factory: seleção por configuração, não o Factory Method GoF.
export function criarProdutoRepository({ tipo, caminho }) {
  const tipoNormalizado = tipo ? tipo.toString().toLowerCase() : '';

  if (tipoNormalizado === 'csv') {
    return new CsvProdutoRepository(caminho);
  }

  if (tipoNormalizado === 'sqlite') {
    return new SqliteProdutoRepository(caminho);
  }

  throw new Error(`Tipo de persistência desconhecido: "${tipo}". Tipos suportados: "csv", "sqlite".`);
}
