import { readFile, mkdir, writeFile, rename } from 'node:fs/promises';
import { lerCsv } from '../../apoio/csv.js';

const recebido = new URL('./runtime/entrada/produtos.csv', import.meta.url);
const destino = new URL('./runtime/local/produtos.csv', import.meta.url);

try {
  const texto = await readFile(recebido, 'utf8');
  const produtos = lerCsv(texto);

  // Validando cada linha do arquivo recebido
  const skusVistos = new Set();

  for (const produto of produtos) {
    const { sku, nome, quantidade } = produto;

    // 1. Validar SKU: não vazio e sem duplicados
    if (!sku || typeof sku !== 'string' || sku.trim() === '') {
      throw new Error('Importação rejeitada: existe produto com SKU vazio.');
    }
    if (skusVistos.has(sku)) {
      throw new Error(`Importação rejeitada: SKU duplicado encontrado (${sku}).`);
    }
    skusVistos.add(sku);

    // 2. Validar Nome: não vazio
    if (!nome || typeof nome !== 'string' || nome.trim() === '') {
      throw new Error(`Importação rejeitada: produto ${sku} está com o nome vazio.`);
    }

    // 3. Validar Quantidade: inteira, não nula/vazia e >= 0
    const qtdNum = Number(quantidade);
    if (
      quantidade === '' ||
      quantidade === null ||
      quantidade === undefined ||
      Number.isNaN(qtdNum) ||
      !Number.isInteger(qtdNum) ||
      qtdNum < 0
    ) {
      throw new Error(`Importação rejeitada: quantidade inválida para o produto ${sku}.`);
    }
  }

  // Se todas as validações passarem, substitui o snapshot local
  await mkdir(new URL('./runtime/local/', import.meta.url), { recursive: true });
  const temporario = new URL('./runtime/local/produtos.tmp', import.meta.url);
  await writeFile(temporario, texto, 'utf8');
  await rename(temporario, destino);
  
  console.log(`Importados ${produtos.length} produtos. Snapshot substituído.`);
} catch (erro) {
  console.error(erro.message);
  process.exitCode = 1;
}