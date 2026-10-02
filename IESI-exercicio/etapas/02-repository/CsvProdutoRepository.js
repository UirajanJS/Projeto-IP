import { readFile, writeFile, rename } from 'node:fs/promises';
import { lerCsv, escreverCsv } from '../../apoio/csv.js';

export class CsvProdutoRepository {
  constructor(caminho) {
    this.caminho = caminho;
  }

  async listar() {
    try {
      const conteudo = await readFile(this.caminho, 'utf8');
      const produtos = lerCsv(conteudo);

      return produtos
        .map((p) => ({
          ...p,
          quantidade: Number(p.quantidade)
        }))
        .sort((a, b) => a.sku.localeCompare(b.sku));
    } catch (erro) {
      if (erro.code === 'ENOENT') {
        return [];
      }
      throw erro;
    }
  }

  async buscarPorSku(sku) {
    const produtos = await this.listar();
    const produto = produtos.find((p) => p.sku === sku);
    return produto || null;
  }

  async baixarEstoque(sku, quantidade) {
    const produtos = await this.listar();
    const produto = produtos.find((p) => p.sku === sku);

    if (!produto) {
      const erro = new Error(`Produto não encontrado para o SKU: ${sku}`);
      erro.codigo = 'PRODUTO_INEXISTENTE';
      throw erro;
    }

    if (produto.quantidade < quantidade) {
      const erro = new Error(`Saldo insuficiente para o SKU ${sku}. Disponível: ${produto.quantidade}, Solicitado: ${quantidade}`);
      erro.codigo = 'SALDO_INSUFICIENTE';
      throw erro;
    }

    // Atualiza a quantidade do produto selecionado
    produto.quantidade -= quantidade;

    // Prepara a gravação atômica do novo snapshot em CSV
    const textoCsv = escreverCsv(produtos);
    const caminhoTemp = new URL(`${this.caminho.href}.tmp`);

    await writeFile(caminhoTemp, textoCsv, 'utf8');
    await rename(caminhoTemp, this.caminho);

    return { ...produto };
  }

  close() {}
}