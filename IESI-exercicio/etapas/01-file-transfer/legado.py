"""Sistema produtor em Python. Execute a partir da raiz do projeto."""
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parent
ORIGEM = BASE.parent.parent / 'dados' / 'produtos.csv'
SAIDA = BASE / 'runtime' / 'saida' / 'produtos.csv'

def exportar():
    with ORIGEM.open(encoding='utf-8', newline='') as arquivo:
        produtos = list(csv.DictReader(arquivo))
    
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    
    # Arquivo temporário no mesmo diretório para garantir escrita atômica
    temp_path = SAIDA.with_suffix('.tmp')
    
    # Escreve primeiro no arquivo temporário
    with temp_path.open('w', encoding='utf-8', newline='') as temp_file:
        fieldnames = ['sku', 'nome', 'quantidade']
        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        
        writer.writeheader()
        for produto in produtos:
            writer.writerow({
                'sku': produto['sku'],
                'nome': produto['nome'],
                'quantidade': produto['quantidade']
            })
            
    # Substitui atomicamente o arquivo temporário pelo final
    # O consumidor nunca verá o arquivo parcialmente escrito
    temp_path.replace(SAIDA)

if __name__ == '__main__':
    exportar()
    print(f'Snapshot publicado: {SAIDA}')
