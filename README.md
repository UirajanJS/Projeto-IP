# Projeto-IP
Projeto final da disciplina de Introdução á Programação

Título do projeto: MINECIN

Membros da equipe: 
João Victor Presbytero <jvpacqg>
Maria Rosicler Lúcia de Lima <mrll>
Pierre Antônio da Silva<pas2>
Rafael Cardoso Clementino de Siqueira <rccs2>
Uirajan José da Silva <ujs>

#A descrição da arquitetura do projeto:
O MINECIN é um divertido jogo desenvolvido na linguagem python com a utilização da biblioteca pygame, onde o jogador assume o papel
de um minerador astuto que busca dentre tantas façanhas alcançar a tão desejada riqueza, nem que para isso precise atrapalhar qualquer outro ganancioso que entre em seu caminho
No MINECIN não há espaço para divisões, o egoísmo é sua única arma e ela deve ser usada para conseguir coletar a maior quantidade possível de minerios que podem ser de 3 tipos
(ouro em sua forma impura(o mais valioso), cobre na forma de calcopirita(valor intermediário) e não menos importante, o ferro na forma de magnetita(menos valioso)). 
Esta disputa irá adentrar nas mais temidas e desafiadoras minas que qualquer minerador experiente exitaria em pisar, em um ambiente hostil onde há dois mineradores ávidos por minério, apenas um deles
será sagrado vencedor, aquele que conseguir o maior valor de minério possível.

#Explicando como o código foi organizado


#As capturas de tela do sistema funcionando para compor a galeria de projetos:
FASE DE DESENVOLVIMENTO:
<table>
  <tr>
    <td><img src="src/screenshots/teste%20de%20frames%20para%20os%20objetos.png" width="250"></td>
    <td><img src="src/screenshots/teste%20direcionamento%20e%20durabilidade.png" width="250"></td>
  </tr>
  <tr>
    <td><img src="src/screenshots/teste%20durabilidade%20rochas.png" width="250"></td>
    <td><img src="src/screenshots/teste%20interação%20pedras.png" width="250"></td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="src/screenshots/dinamica%20fisica%20quase%20pronta.png"</td>
  </tr>
</table>


FASE DE IMPLEMENTAÇÃO:
loading...

#As ferramentas, bibliotecas, frameworks utilizados com as respectivas justificativas para o uso;
*Linguagem de Programação: 
A linguiagem de programação escolhida foi o Python, por conveniencia da disciplina de Introdução a lógica de programação(IP) 
do primeiro período da disciplina de Ciência da Computação do Centro de Informática da UFPE.
*Módulos:
O principal módulo utilizado para o desenvolveomento foi o Pygame, por sugestão de praticidade e por permitir desenvolver num curto espaço de tempo, além da 
flexibilidade de se trabalhar com arte pixelada que também facilita a usabilidade do módulo.
O módulo random foi utilizado para gerar aleatoriedade(através da função randint()) no que tange a durabilidade das rochas e sua distribuição
O módulo sys foi utilizado para permitir o controle da tela(fechamento) através da função exit().

#A divisão de trabalho dentro do grupo (quem fez o quê);
<table>
  <tr>
    <th>MEMBRO</th>
    <th>FUNÇÃO INICIAL ATRIBUÍDA</th>
    <th>O QUE FEZ</th>
  </tr>
  
  <tr>
    <td>João Victor Presbytero </td>
    <td>Designer de Nível</td>
    <td>Responsável por montar o mapa inicial do jogo (o mundo de mineração), 
        Implementar componentes e solucionar problemas de integração
    </td>
  </tr>
  
  <tr>
    <td>Maria Rosicler Lúcia de Lima</td>
    <td>Designer de Mecânicas</td>
    <td>Lógica de mineração (interação com blocos), o sistema de inventário 
    (contagem dos 3 coletáveis) e a condição de vitória/fim de jogo.
    </td>
  </tr

  <tr>
    <td>Pierre Antônio da Silva</td>
    <td>Designer de Som</td>
    <td>Edição dos sons e música do jogo</td>
  </tr>
  
  <tr>
    <td>Rafael Cardoso Clementino de Siqueira</td>
    <td>Arquiteto de Jogo / Programador Líder</td>
    <td>Definiu a estrutura central (loop principal, estados), gerenciou a integração dos componentes
        garantiu a comunicação entre os módulos (player, mundo, UI), e também solucionou os problemas de integração.
    </td>
  </tr>
  
  <tr>
    <td>Uirajan José da Silva</td>
    <td>Designer de Assets</td>
    <td>Criou os gráficos em pixel art, assets visuais, ícones dos coletáveis 
        (sprites do jogador, blocos, os 3 coletáveis, mapa) e elementos de UI.
    </td>
  </tr>
</table>


#Os conceitos que foram apresentados durante a disciplina e utilizados no projeto (indicando onde foram usados);
No projeto, excetuando a parte de programação orientada a objeto, todas os conceitos aprendidos foram utilizados direta ou indiretamente,
sendo portanto destacados na tabela a seguir:
<table>
  <tr>
    <th>CONCEITO APRENDIDO</th>
    <th>ONDE FOI UTILIZADO</th>
  </tr>
  <tr>
    <td>LAÇOS DE REPETIÇÃO</td>
    <td>CICLO DE EXECUÇÃO DO JOGO</td>
  </tr>
</table>

#Os desafios e erros enfrentados no decorrer do projeto e as lições aprendidas. Para tanto, respondam às seguintes perguntas:
#Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
#Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
Organização sem dúvida foi um problema pois o tempo foi relativamente curto para desenvolver. Conseguimos estabelecer uma comunicação mais dinâmica na porção final
do desenvolvimento e isso ajudou bastante na conclusão dos objetivos.

#Quais as lições aprendidas durante o projeto?
Desenvolver um jogo por mais simples que seja,exige muita disciplina, tempo e organização, onde cada etapa otimizada através da cooperação leva a uma
maior propensão da aplicação ser bem sucedida.
A curva de aprendizado da ferramenta utilizada é baixa, permitindo o desenvolvimento de jogos simples em poucos dias. 

