import { abrirBanco } from '../../apoio/sqlite.js';

export class SqliteProdutoRepository {
  constructor(caminho) {
    this.db = abrirBanco(caminho);
  }

  async listar() {
    const stmt = this.db.prepare('SELECT sku, nome, quantidade FROM produtos ORDER BY sku ASC');
    const linhas = stmt.all();

    return linhas.map((linha) => ({
      sku: linha.sku,
      nome: linha.nome,
      quantidade: Number(linha.quantidade)
    }));
  }

  async buscarPorSku(sku) {
    const stmt = this.db.prepare('SELECT sku, nome, quantidade FROM produtos WHERE sku = ?');
    const linha = stmt.get(sku);

    if (!linha) {
      return null;
    }

    return {
      sku: linha.sku,
      nome: linha.nome,
      quantidade: Number(linha.quantidade)
    };
  }

  async baixarEstoque(sku, quantidade) {
    // Inicia transação garantindo bloqueio para escrita concorrente
    this.db.exec('BEGIN IMMEDIATE');

    try {
      // Tenta a baixa atômica apenas se o produto existir e tiver saldo suficiente
      const updateStmt = this.db.prepare(
        'UPDATE produtos SET quantidade = quantidade - ? WHERE sku = ? AND quantidade >= ?'
      );
      const resultado = updateStmt.run(quantidade, sku, quantidade);

      // Se nenhuma linha foi alterada, precisamos descobrir o motivo dentro da mesma transação
      if (resultado.changes === 0) {
        const checkStmt = this.db.prepare('SELECT quantidade FROM produtos WHERE sku = ?');
        const produtoAtual = checkStmt.get(sku);

        if (!produtoAtual) {
          const erro = new Error(`Produto não encontrado para o SKU: ${sku}`);
          erro.codigo = 'PRODUTO_INEXISTENTE';
          throw erro;
        } else {
          const erro = new Error(
            `Saldo insuficiente para o SKU ${sku}. Disponível: ${produtoAtual.quantidade}, Solicitado: ${quantidade}`
          );
          erro.codigo = 'SALDO_INSUFICIENTE';
          throw erro;
        }
      }

      // Busca o produto atualizado após o UPDATE bem-sucedido
      const selectStmt = this.db.prepare('SELECT sku, nome, quantidade FROM produtos WHERE sku = ?');
      const produtoAtualizado = selectStmt.get(sku);

      // Confirma as alterações no banco
      this.db.exec('COMMIT');

      return {
        sku: produtoAtualizado.sku,
        nome: produtoAtualizado.nome,
        quantidade: Number(produtoAtualizado.quantidade)
      };
    } catch (erro) {
      // Em caso de erro, desfaz a transação e repassa a exceção
      this.db.exec('ROLLBACK');
      throw erro;
    }
  }

  close() {
    this.db.close();
  }
}