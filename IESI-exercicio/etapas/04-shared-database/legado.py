"""Acesso direto ao MESMO banco usado pelo console Node, em outra conexão."""
import sqlite3
from pathlib import Path

BANCO = Path(__file__).resolve().parent / 'runtime' / 'estoque.db'

def baixar(conexao, sku, quantidade):
    # 1. Validação dos parâmetros de entrada
    if not sku or not isinstance(sku, str) or not sku.strip():
        raise ValueError('ENTRADA_INVALIDA: SKU deve ser informado e não pode ser vazio.')
    
    if not isinstance(quantidade, int) or quantidade <= 0:
        raise ValueError('ENTRADA_INVALIDA: A quantidade deve ser um número inteiro positivo.')

    sku = sku.strip()

    try:
        # Inicia transação explícita com bloqueio imediato para escrita
        conexao.execute('BEGIN IMMEDIATE')

        # Tenta a baixa atômica via SQL condicional (garante consistência mesmo com escritas concorrentes)
        cursor = conexao.execute(
            'UPDATE produtos SET quantidade = quantidade - ? WHERE sku = ? AND quantidade >= ?',
            (quantidade, sku, quantidade)
        )

        # Se nenhuma linha foi afetada, identifica se foi por SKU inexistente ou Saldo Insuficiente
        if cursor.rowcount == 0:
            cursor_check = conexao.execute('SELECT quantidade FROM produtos WHERE sku = ?', (sku,))
            produto = cursor_check.fetchone()

            if produto is None:
                raise ValueError(f'PRODUTO_INEXISTENTE: Produto não encontrado para o SKU: {sku}')
            else:
                saldo_atual = produto[0]
                raise ValueError(
                    f'SALDO_INSUFICIENTE: Saldo insuficiente para o SKU {sku}. '
                    f'Disponível: {saldo_atual}, Solicitado: {quantidade}'
                )

        # Confirma as alterações na mesma transação
        conexao.commit()
        print(f'Baixa de {quantidade} unidade(s) do SKU {sku} realizada com sucesso!')

    except Exception:
        # Em qualquer falha, desfaz a transação
        conexao.rollback()
        raise

if __name__ == '__main__':
    if not BANCO.exists():
        raise SystemExit('Execute preparar.js desta etapa antes de abrir o legado.')
    with sqlite3.connect(BANCO, timeout=3) as conexao:
        print(conexao.execute('SELECT sku,nome,quantidade FROM produtos ORDER BY sku').fetchall())
        sku = input('SKU para baixa: ')
        quantidade = int(input('Quantidade: '))
        baixar(conexao, sku, quantidade)