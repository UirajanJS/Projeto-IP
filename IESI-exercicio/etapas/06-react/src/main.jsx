import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';

function App() {
  const [produtos, setProdutos] = useState([]);
  const [sku, setSku] = useState('P003');
  const [quantidade, setQuantidade] = useState(1);
  const [mensagem, setMensagem] = useState('');
  const [ocupado, setOcupado] = useState(false);

  async function listar() {
    // UI-1: Consome o endpoint GET /produtos utilizando rota relativa
    const response = await fetch('/produtos');
    const dados = await response.json();

    if (!response.ok) {
      throw new Error(dados.erro || 'Falha ao carregar lista de produtos.');
    }

    setProdutos(dados);
    setMensagem('Lista de produtos atualizada com sucesso.');
  }

  async function baixar(evento) {
    // UI-2: Solicita a operação de baixa enviando POST /estoque/baixas
    const response = await fetch('/estoque/baixas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sku, quantidade })
    });

    const dados = await response.json();

    if (!response.ok) {
      throw new Error(dados.erro || 'Falha ao realizar a baixa no estoque.');
    }

    setMensagem(`Baixa realizada! Produto ${dados.nome} (SKU: ${dados.sku}) agora possui saldo ${dados.quantidade}.`);
    
    // Recarrega a lista para refletir a alteração
    await listar();
  }

  async function executar(acao) {
    setOcupado(true);
    try {
      await acao();
    } catch (erro) {
      setMensagem(erro.message);
    } finally {
      setOcupado(false);
    }
  }

  return (
    <main style={{ maxWidth: 640, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>Estoque de produtos</h1>
      <button disabled={ocupado} onClick={() => executar(listar)}>
        Atualizar estoque
      </button>
      <ul>
        {produtos.map((p) => (
          <li key={p.sku}>
            {p.sku} — {p.nome}: {p.quantidade}
          </li>
        ))}
      </ul>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          executar(() => baixar(e));
        }}
      >
        <label>
          SKU <input value={sku} onChange={(e) => setSku(e.target.value)} />
        </label>{' '}
        <label>
          Quantidade{' '}
          <input
            type="number"
            min="1"
            step="1"
            value={quantidade}
            onChange={(e) => setQuantidade(Number(e.target.value))}
          />
        </label>{' '}
        <button disabled={ocupado}>Baixar estoque</button>
      </form>
      <p role="status">{mensagem}</p>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<App />);