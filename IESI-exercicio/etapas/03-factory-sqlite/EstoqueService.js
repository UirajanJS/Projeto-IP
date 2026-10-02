export class EstoqueService {
  constructor(repository) {
    this.repository = repository;
  }

  listar() {
    return this.repository.listar();
  }

  buscarPorSku(sku) {
    return this.repository.buscarPorSku(sku);
  }

  async baixarEstoque(sku, quantidade) {
    // 1. Validar se SKU é uma string válida e não vazia
    if (!sku || typeof sku !== 'string' || sku.trim() === '') {
      const erro = new Error('O SKU deve ser informado e não pode ser vazio.');
      erro.codigo = 'ENTRADA_INVALIDA';
      throw erro;
    }

    // 2. Validar se quantidade é um número inteiro positivo (> 0)
    const qtdNum = Number(quantidade);
    if (
      quantidade === '' ||
      quantidade === null ||
      quantidade === undefined ||
      Number.isNaN(qtdNum) ||
      !Number.isInteger(qtdNum) ||
      qtdNum <= 0
    ) {
      const erro = new Error('A quantidade para baixa deve ser um número inteiro positivo.');
      erro.codigo = 'ENTRADA_INVALIDA';
      throw erro;
    }

    // 3. Delegar a baixa condicional diretamente para o Repository
    return await this.repository.baixarEstoque(sku.trim(), qtdNum);
  }
}