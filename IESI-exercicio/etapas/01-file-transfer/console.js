import { readFile } from 'node:fs/promises';
import { lerCsv } from '../../apoio/csv.js';
import { executarConsole } from '../../apoio/console.js';

// Versão inicial propositalmente acoplada ao CSV: refatorada na etapa 02.
async function carregar() {
  return lerCsv(await readFile(new URL('./runtime/local/produtos.csv', import.meta.url), 'utf8'))
    .map(p => ({ ...p, quantidade: Number(p.quantidade) }));
}

await executarConsole({
  listar: carregar,
  async buscarPorSku(sku) {
    const produtos = await carregar();
    const produto = produtos.find(p => p.sku === sku);
    return produto || null;
  }
});
