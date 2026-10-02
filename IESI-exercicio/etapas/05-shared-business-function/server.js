import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { criarProdutoRepository } from './repositoryFactory.js';
import { EstoqueService } from './EstoqueService.js';

const repository = criarProdutoRepository({
  tipo: 'sqlite',
  caminho: fileURLToPath(new URL('./runtime/estoque.db', import.meta.url))
});
const service = new EstoqueService(repository);

function responder(res, status, dados) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(dados));
}

async function lerJson(req) {
  let texto = '';
  for await (const parte of req) {
    texto += parte;
    if (texto.length > 10000) throw new Error('Corpo muito grande.');
  }
  return JSON.parse(texto);
}

const server = createServer(async (req, res) => {
  try {
    if (req.method === 'GET' && req.url === '/produtos') {
      return responder(res, 200, await service.listar());
    }

    if (req.method === 'POST' && req.url === '/estoque/baixas') {
      const dados = await lerJson(req);

      // API-1: Delega a baixa de estoque ao serviço de domínio e retorna o produto atualizado
      const produtoAtualizado = await service.baixarEstoque(dados?.sku, dados?.quantidade);
      return responder(res, 200, produtoAtualizado);
    }

    responder(res, 404, { erro: 'Rota inexistente' });
  } catch (erro) {
    // API-2: Mapeia exceções de domínio/JSON para os status HTTP correspondentes
    
    // 1. JSON malformatado ou dados de entrada inválidos (ex: SKU vazio, quantidade inválida)
    if (erro instanceof SyntaxError || erro.codigo === 'ENTRADA_INVALIDA' || erro.message === 'Corpo muito grande.') {
      return responder(res, 400, {
        codigo: erro.codigo || 'ENTRADA_INVALIDA',
        erro: erro.message
      });
    }

    // 2. SKU inexistente no cadastro
    if (erro.codigo === 'PRODUTO_INEXISTENTE') {
      return responder(res, 404, {
        codigo: erro.codigo,
        erro: erro.message
      });
    }

    // 3. Saldo de estoque insuficiente
    if (erro.codigo === 'SALDO_INSUFICIENTE') {
      return responder(res, 409, {
        codigo: erro.codigo,
        erro: erro.message
      });
    }

    // 4. Erros internos do servidor
    responder(res, 500, {
      codigo: 'ERRO_INTERNO',
      erro: erro.message || 'Falha interna do servidor'
    });
  }
});

server.listen(3000, '127.0.0.1', () => console.log('API em http://127.0.0.1:3000'));

process.on('SIGINT', () =>
  server.close(() => {
    repository.close();
    process.exit(0);
  })
);