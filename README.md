Qual é o contrato compartilhado em cada etapa: arquivo, esquema ou API?

Etapa 01: Layout e sintaxe do arquivo CSV (sku,nome,quantidade).

Etapa 02 & 03: Contrato de interface da classe/módulo Repository em JavaScript.

Etapa 04: Esquema de banco de dados relacional SQL (tabelas, colunas e tipos em estoque.db).

Etapa 05 & 06: Contrato de API REST HTTP/JSON (endpoints GET /produtos e POST /estoque/baixas).

Quando uma alteração de estoque se torna visível para o outro sistema?

Etapa 01: Somente após a publicação do CSV pelo produtor, transporte até a pasta de entrada e execução manual do script de importação pelo consumidor.

Etapas 02 e 03 (CSV): Imediatamente para novos processos lidos localmente, mas isolado do sistema legado.

Etapa 04: Imediatamente após o COMMIT da transação SQL no banco compartilhado.

Etapas 05 e 06: Imediatamente para qualquer cliente que consulte a API após o término do POST.

Onde a regra que impede saldo negativo é executada e quem pode contorná-la?

Nas Etapas 01 a 04, a regra é duplicada na camada de aplicação (Node e Python) e/ou na cláusula WHERE saldo >= quantidade das queries. Qualquer cliente com acesso direto de escrita ao arquivo/banco pode contorná-la alterando os dados diretamente.

Nas Etapas 05 e 06, a regra é centralizada unicamente no Serviço/API da aplicação Node. Nenhum cliente HTTP pode contorná-la, pois não possui acesso direto ao banco subjacente.

O que ocorre se dois clientes tentarem comprar a última unidade?

No CSV (Etapas 01 a 03): Condição de corrida (race condition). O último arquivo gravado sobrescreve o anterior (perda de atualizações / lost update).

No SQLite (Etapas 04 e 05): A concorrência é tratada por trava de transação (BEGIN IMMEDIATE). A primeira transação decrementa o saldo para 0. A segunda falha no UPDATE condicional, resultando em erro de SALDO_INSUFICIENTE (HTTP 409 na API).

Quais dependências mudam ao evoluir de dados compartilhados para uma função compartilhada?

Deixa-se de depender da estrutura física interna do banco de dados (tabelas, locks, drivers de banco) e passa-se a depender do protocolo de rede (HTTP), do formato das mensagens (JSON) e da disponibilidade operacional do servidor de API.

Por que Repository e Factory ajudam a evolução do código, mas não resolvem sozinhos os problemas de integração?

O Repository e a Factory isolam o código da aplicação dos detalhes de persistência local (trocar CSV por SQLite sem alterar a regra de negócio). No entanto, são padrões internos de arquitetura de software de um único processo; eles não resolvem problemas de rede, concorrência distribuída, acoplamento de esquema ou comunicação entre diferentes sistemas.




1. Gerar a exportação no Python:
   ```sh
   python3 etapas/01-file-transfer/legado.py




Simular a entrega do arquivo para a entrada do consumidor:

Bash
mkdir -p etapas/01-file-transfer/runtime/entrada
cp etapas/01-file-transfer/runtime/saida/produtos.csv etapas/01-file-transfer/runtime/entrada/produtos.csv
Processar a importação e consultar o console Node:

Bash
node etapas/01-file-transfer/importar.js
node etapas/01-file-transfer/console.js
Etapa 02 — Repository e Serviço (CSV)
Preparar o ambiente local:

Bash
mkdir -p etapas/02-repository/runtime
cp dados/produtos.csv etapas/02-repository/runtime/produtos.csv
Executar o console interativo:

Bash
node etapas/02-repository/console.js
Etapa 03 — Factory e SQLite
Preparar os dados de execução:

Bash
node etapas/03-factory-sqlite/preparar.js
Executar o console alternando a persistência via variável de ambiente:

Bash
# Execução via CSV
PERSISTENCIA=csv node etapas/03-factory-sqlite/console.js

# Execução via SQLite
PERSISTENCIA=sqlite node etapas/03-factory-sqlite/console.js
Etapa 04 — Shared Database
Preparar o banco de dados SQLite compartilhado:

Bash
node etapas/04-shared-database/preparar.js
Executar o cliente Node em um terminal:

Bash
node etapas/04-shared-database/console.js
Executar o cliente Python em outro terminal:

Bash
python3 etapas/04-shared-database/legado.py
Etapa 05 — Shared Business Function por HTTP (API REST)
Preparar e iniciar o servidor API Node:

Bash
node etapas/05-shared-business-function/preparar.js
node etapas/05-shared-business-function/server.js
Em outro terminal, executar um dos clientes HTTP:

Bash
# Cliente Node
node etapas/05-shared-business-function/console.js

# Cliente Python
python3 etapas/05-shared-business-function/legado.py
(Opcional) Testar manualmente via curl:

Bash
# Listar produtos
curl [http://127.0.0.1:3000/produtos](http://127.0.0.1:3000/produtos)

# Realizar baixa de estoque
curl -i -X POST [http://127.0.0.1:3000/estoque/baixas](http://127.0.0.1:3000/estoque/baixas) \
  -H 'Content-Type: application/json' \
  -d '{"sku":"P003","quantidade":1}'
Etapa 06 — React Frontend
Com a API da Etapa 05 em execução, abra um novo terminal:

Bash
cd etapas/06-react
npm install
npm run dev
Acesse a URL informada pelo Vite (ex: http://localhost:5173).

Para validar a build final da aplicação:

Bash
npm run build
🔍 Verificação de Código e Sintaxe
Para verificar a sintaxe dos arquivos .js e .mjs do projeto, execute na raiz:

Bash
npm run verificar
