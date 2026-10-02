"""Cliente legado: agora solicita a função via HTTP, sem acesso ao banco."""
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def baixar(sku, quantidade):
    url = 'http://127.0.0.1:3000/estoque/baixas'
    
    payload = json.dumps({'sku': sku, 'quantidade': quantidade}).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    req = Request(url, data=payload, headers=headers, method='POST')
    
    try:
        # Define timeout curto de conexao/resposta (ex: 5 segundos)
        with urlopen(req, timeout=5) as resposta:
            dados = json.loads(resposta.read().decode('utf-8'))
            return dados

    except HTTPError as e:
        # A API respondeu com status 4xx ou 5xx
        corpo = e.read().decode('utf-8')
        try:
            dados_erro = json.loads(corpo)
            mensagem = dados_erro.get('erro', 'Erro desconhecido na API')
            codigo = dados_erro.get('codigo', 'ERRO_HTTP')
        except Exception:
            mensagem = corpo or str(e)
            codigo = 'ERRO_HTTP'

        raise ValueError(f'{codigo}: {mensagem}') from e

    except URLError as e:
        # Falha de rede, timeout ou servidor fora do ar.
        # ATENÇÃO: Falta de resposta não garante que a baixa não foi processada!
        raise RuntimeError(f'Falha na comunicação com o serviço (/estoque/baixas): {e.reason}') from e

if __name__ == '__main__':
    print(baixar(input('SKU: '), int(input('Quantidade: '))))