import { executarConsole } from '../../apoio/console.js';
import { pendente } from '../../apoio/exercicio.js';

const base = 'http://127.0.0.1:3000';

// Este cliente conhece HTTP; não importa Repository nem abre SQLite.
await executarConsole({
  async listar() {
    const res = await fetch(`${base}/produtos`);
    const dados = await res.json();
    if (!res.ok) throw new Error(dados.erro);
    return dados;
  },
  async buscarPorSku(sku) { 
    return (await this.listar()).find(p => p.sku === sku) ?? null; 
  },
  async baixarEstoque(sku, quantidade) {
    const res = await fetch(`${base}/estoque/baixas`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sku, quantidade })
    });

    const dados = await res.json();

    if (!res.ok) {
      const erro = new Error(dados.erro || 'Falha ao realizar baixa no estoque');
      erro.codigo = dados.codigo;
      throw erro;
    }

    return dados;
  }
}, { permitirBaixa: true });