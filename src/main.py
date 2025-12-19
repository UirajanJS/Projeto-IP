import random
import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura=680
altura=680
pygame.display.set_caption("MINECIn")
tela=pygame.display.set_mode((largura, altura))

tela_inicial = pygame.image.load("tela_inicial.png") #Essa linha carrega a imagem com o caminho para ela
tela_inicial = pygame.transform.scale(tela_inicial, (largura, altura)) #redimensiona a imagem para ocupar a tela do jogo

fonte = pygame.font.SysFont("arial",12,True,False)

#não fazer tamanhos ímpares, por causa da parte da picareta
x_jog=26
y_jog=26

#para ser usado em um lado
count=[80, 7, 3, 10, 27] #soma igual a 127 pois exclui o lugar do jogador
valores=["P","M","O","C","N"]
ordem=[]

size_pedra=40

#parametros
M="M"
O="O"
C="C"
X="X"
N="N"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNÇÕES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def tela_historia():
    fonte_texto = pygame.font.Font(None, 32)
    
    historia = [
        "A historinha",
        "e o objetivo do jogo",
        "é explicado ao jogador por aqui..."
    ]

    frases_concluidas = []

    #percorre as linhas da historia
    for indice_linha, linha in enumerate(historia):
        texto_escrevendo = ""
        for letra in linha:
            texto_escrevendo += letra

            tela.fill((0, 0, 0))                                                            #limpa  atela

            #renderiza as frases concluidas
            for indice_frase, frase in enumerate(frases_concluidas):
                texto_render = fonte_texto.render(frase, True, (200, 200, 200))
                x = largura//2 - texto_render.get_width()//2                                #centralizar as linhas
                y = 150 + indice_frase*40
                tela.blit(texto_render, (x, y))

            #renderiza a frase atual a ser digitada
            texto_render = fonte_texto.render(texto_escrevendo, True, (200, 200, 200))
            x = largura//2 - texto_render.get_width()//2
            y = 150 + indice_linha*40
            tela.blit(texto_render, (x, y))            

            pygame.display.flip()
            pygame.time.delay(100)                                                          #velocidade da digitação

        #adiciona frase concluida na lista de concluídas
        frases_concluidas.append(linha)
        pygame.time.delay(1000)                                                             #pausa entre frases

    transicao()
    tela_de_inicio()


""" É permitido usar Surface e set.alpha? """
def transicao():
    for i in range(0, 255, 15):                     #começa em 0 até 255, de 15 em 15 (utilizado para calcular a transparencia)
        tela.fill((0,0,0))                          #limpa a tela
       
        tela.blit(tela_inicial, (0, 0))             #desenha a imagem inicial
        
        camada = pygame.Surface((largura, altura))  #cria uma superficie (Surface) do tamanho da tela
        camada.fill((0,0,0))                        #pinta ela de preto
        camada.set_alpha(255 - i)                   #set.alpha controla (0 invisivel, 255 opaco) com o i
        tela.blit(camada, (0,0))                    #superficie preta com transparencia é desenhada por cima da tela

        pygame.display.update()
        pygame.time.delay(150)                      #velocidade da transição


def tela_de_inicio():
    fonte_titulo = pygame.font.Font(None, 74)
    fonte_instrucao = pygame.font.Font(None, 36)
    rodando = True
    
    while rodando:
        tela.blit(tela_inicial, (0, 0))  #imagem png salva no mesmo endereço do jogo
        
        titulo = fonte_titulo.render("MineCIn", True, (255, 255, 255)) #Título e instrução cor verde
        instrucao = fonte_instrucao.render("Pressione ENTER para começar", True, (255, 255, 255))
        
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, altura//3))
        tela.blit(instrucao, (largura//2 - instrucao.get_width()//2, altura//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  
                    rodando = False

def mapear():
    objeto=""
    for y in range(16):
        for x in range(17):
            objeto = mapa[y][x]
            print(objeto)
            if type(objeto)==int:
                rect_pedras.append(Pedra(x*40,y*40,objeto))
                rect_pedras[-1].definir()
            elif objeto=="M":
                rect_pedras.append(Magnetita(x*40,y*40))
                rect_pedras[-1].definir()
            elif objeto=="O":
                rect_pedras.append(Ouro(x*40,y*40))
                rect_pedras[-1].definir()
            elif objeto=="C":
                rect_pedras.append(Cobre(x*40,y*40))
                rect_pedras[-1].definir()
            elif objeto=="X":
                rect_pedras.append(Muro(x*40,y*40))
                rect_pedras[-1].definir()
            elif objeto=="N":
                pass
            else:
                print(objeto)
                print("erro")
            

def espelhar():
    for y in range(16):
        for x in range(8):
            mapa[y][-x-1]=mapa[y][x]

def construir():
    a=0
    b=0
    c=False
    for i in range(127):
        c=False
        a=random.randrange(sum(count))
        for f in range(len(count)):
            if c==False:
                if count[f]>a:
                    a=f
                    c=True
                else:
                    a-=count[f]
        
        if valores[a]=="P":
            b=random.randrange(11)
            if b<6:
                ordem.append(15)
            elif b<10:
                ordem.append(22)
            else:
                ordem.append(31)
        else:
            ordem.append(valores[a])
        count[a]-=1
        if count[a]==0:
            valores.pop(a)
            count.pop(a)
    
    
    a=0
    for y in range(16):
        for x in range(8):
            #vai bloco por bloco, mas não coloca no lugar do jogador
            if not(y==15 and x==0):
                #print(f"a={a}, x={x}, y={y}")
                mapa[y][x]=ordem[a]
                a+=1


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MINÉRIOS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Pedra (pygame.sprite.Sprite):
    def __init__(self,x_pedra,y_pedra,durabilidade=1):
        pygame.sprite.Sprite.__init__(self)
        #propriedades básicas
        self.durabilidade=durabilidade
        self.x=x_pedra
        self.y=y_pedra
        self.image=0
        self.cor=(0,0,0)
        self.rect="" #objeto retângulo
    
    #desenhar a pedra na tela
    def definir(self):
        pass
    def mostrar (self):
        self.cor=(140-self.durabilidade*4,140-self.durabilidade*4,140-self.durabilidade*4)
        self.rect=pygame.draw.rect(tela,self.cor,(self.x,self.y,size_pedra,size_pedra))
    
    #função chamada para reduzir a durabilidade
    def quebrar (self, nome):
        self.durabilidade-=nome.dano_picareta
        if self.durabilidade<=0:
            nome.items["Pedra"]+=2
            rect_pedras.remove(self)
    def restaurar (self, nome):
        while (self.durabilidade<=31) and (nome.items["Pedra"]>0):
            self.durabilidade+=1
            nome.items["Pedra"]-=1

class Magnetita(Pedra):
    def definir (self):
        self.image=pygame.image.load("minerio_magnetita.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)
    
    #função chamada para reduzir a durabilidade
    def quebrar (self,nome):
        nome.items["Magnetita"]+=1
        nome.dano_picareta=1+(nome.items["Magnetita"]//2)
        rect_pedras.remove(self)
        self.kill()
        print(nome.items)

class Cobre(Pedra):
    def definir (self):
        self.image=pygame.image.load("minerio_cobre.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)
    
    #função chamada para reduzir a durabilidade
    def quebrar (self,nome):
        nome.items["Cobre"]+=1
        rect_pedras.remove(self)
        self.kill()
        print(nome.items)

class Ouro(Pedra):
    def definir (self):
        self.image=pygame.image.load("minerio_ouro.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)
    
    #função chamada para reduzir a durabilidade
    def quebrar (self,nome):
        nome.items["Ouro"]+=1
        rect_pedras.remove(self)
        self.kill()
        print(nome.items)

class Muro (Pedra):
    def definir (self):
        self.image=pygame.image.load("muro.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)
    
    def quebrar (self, nome):
        pass

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PERSONAGEM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Personagem:
    def __init__(self,x_personagem,y_personagem):
        #propriedades básicas
        self.x=x_personagem
        self.y=y_personagem
        self.picareta=""
        self.x_picareta=0
        self.y_picareta=0
        self.pic_size=0
        self.facing="up"
        self.rect=""
        self.dano_picareta=1
        self.picareta_ativa=False
        self.restaurar_ativa=False
        self.items={"Magnetita":0,"Cobre":0,"Ouro":0, "Pedra":0}
    
    def mostrar(self):
        self.rect=pygame.draw.rect(tela, (0,255,242), (self.x,self.y,x_jog,y_jog))
    def minerar(self,modo):
        
        self.pic_size=16
        
        if self.facing=="up":
            self.x_picareta=self.x+x_jog/2
            self.y_picareta=self.y-self.pic_size
            self.pic_size=1
        
        if self.facing=="down":
            self.x_picareta=self.x+x_jog/2
            self.y_picareta=self.y+y_jog
            self.pic_size=1
        
        if self.facing=="left":
            self.x_picareta=self.x-self.pic_size
            self.y_picareta=self.y+y_jog/2
        
        if self.facing=="right":
            self.x_picareta=self.x+x_jog
            self.y_picareta=self.y+y_jog/2
        
        #desenhar a picareta/
        self.picareta=pygame.draw.rect(tela,(0,255,0),(self.x_picareta,self.y_picareta,self.pic_size,17-self.pic_size))
        if modo=="destruir":
            self.picareta_ativa=True
        elif modo=="restaurar":
            self.restaurar_ativa=True
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ÍCONE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class Icone (pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.x=x_pos
        self.y=y_pos
        self.image=0
        self.rect=0

class Icone_magnetita (Icone):
    def definir (self):
        self.image=pygame.image.load("icone_magnetita.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)

class Icone_cobre (Icone):
    def definir (self):
        self.image=pygame.image.load("icone_cobre.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)

class Icone_ouro (Icone):
    def definir (self):
        self.image=pygame.image.load("icone_ouro.png")
        self.rect=self.image.get_rect()
        self.rect.topleft = self.x, self.y
        todas_as_sprites.add(self)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ JOGO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

jogador = Personagem(0,610)

oponente = Personagem(650,610)

icone_M_e = Icone_magnetita(0,640)
icone_M_d = Icone_magnetita(360,640)

icone_C_e = Icone_cobre(70,640)
icone_C_d = Icone_cobre(430,640)

icone_O_e = Icone_ouro(138,640)
icone_O_d = Icone_ouro(498,640)

todas_as_sprites = pygame.sprite.Group()

icone_M_e.definir()
icone_M_d.definir()
icone_C_e.definir()
icone_C_d.definir()
icone_O_e.definir()
icone_O_d.definir()

mapa=[
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,X,N,N,N,N,N,N,N,N]]

rect_pedras=[]

construir()
espelhar()
mapear()

# <<<outras variáveis>>>
velocidade=5

relogio = pygame.time.Clock()

tela_historia()
tela_de_inicio()

while True:
    #                          Setup de variáveis
    relogio.tick(30)
    tela.fill((0,0,0))
    jogador.picareta_ativa=False
    jogador.restaurar_ativa=False
    oponente.picareta_ativa=False
    oponente.restaurar_ativa=False
    items_jogador=f"             :{jogador.items["Magnetita"]}                    :{jogador.items["Cobre"]}                   :{jogador.items["Ouro"]}                   :{jogador.items["Pedra"]}"
    Placar_esquerdo = fonte.render(items_jogador, False, (255,255,255))
    items_oponente=f"             :{oponente.items["Magnetita"]}                    :{oponente.items["Cobre"]}                   :{oponente.items["Ouro"]}                   :{oponente.items["Pedra"]}"
    Placar_direito = fonte.render(items_oponente, False, (255,255,255))
    
    
    
    #                                 Resposta ao pressionar teclas
    for event in pygame.event.get():
        if event.type==QUIT:
            print(jogador.items)
            print(oponente.items)
            pygame.quit()
            exit()
        if event.type==KEYDOWN:
            if event.key==K_f:
                jogador.minerar("destruir")
            elif event.key==K_g:
                jogador.minerar("restaurar")
            if event.key==K_KP0:
                oponente.minerar("destruir")
            elif event.key==K_KP1:
                oponente.minerar("restaurar")
    
    #                                      movimento do jogador
    if pygame.key.get_pressed()[K_a]:
        jogador.x -= velocidade
        jogador.facing="left"
    if pygame.key.get_pressed()[K_d]:
        jogador.x += velocidade
        jogador.facing="right"
    if pygame.key.get_pressed()[K_s]:
        jogador.y += velocidade
        jogador.facing="down"
    if pygame.key.get_pressed()[K_w]:
        jogador.y -= velocidade
        jogador.facing="up"
    
    #                                       movimento do oponente
    if pygame.key.get_pressed()[K_LEFT]:
        oponente.x -= velocidade
        oponente.facing="left"
    if pygame.key.get_pressed()[K_RIGHT]:
        oponente.x += velocidade
        oponente.facing="right"
    if pygame.key.get_pressed()[K_DOWN]:
        oponente.y += velocidade
        oponente.facing="down"
    if pygame.key.get_pressed()[K_UP]:
        oponente.y -= velocidade
        oponente.facing="up"
    
    #                                       mecânica de parar na borda
    if jogador.y<0:
        jogador.y=0
    if jogador.y>(altura-y_jog-40):
        jogador.y=altura-y_jog-40
    if jogador.x<0:
        jogador.x=0
    if jogador.x>(largura-x_jog):
        jogador.x=largura-x_jog
    
    if oponente.y<0:
        oponente.y=0
    if oponente.y>(altura-y_jog-40):
        oponente.y=altura-y_jog-40
    if oponente.x<0:
        oponente.x=0
    if oponente.x>(largura-x_jog):
        oponente.x=largura-x_jog
    
    
    #                                        mostrar objetos na tela
    jogador.mostrar()
    oponente.mostrar()
    for pedra in rect_pedras:
        if pedra.image==0:
            pedra.mostrar()
    
    
    #                                            colisão com pedras
    for pedra in rect_pedras:
        if jogador.rect.colliderect(pedra.rect):
            if pygame.key.get_pressed()[K_a]:
                jogador.x += velocidade+1
            if pygame.key.get_pressed()[K_d]:
                jogador.x -= velocidade+1
            if pygame.key.get_pressed()[K_s]:
                jogador.y -= velocidade+1
            if pygame.key.get_pressed()[K_w]:
                jogador.y += velocidade+1
        if oponente.rect.colliderect(pedra.rect):
            if pygame.key.get_pressed()[K_LEFT]:
                oponente.x += velocidade+1
            if pygame.key.get_pressed()[K_RIGHT]:
                oponente.x -= velocidade+1
            if pygame.key.get_pressed()[K_DOWN]:
                oponente.y -= velocidade+1
            if pygame.key.get_pressed()[K_UP]:
                oponente.y += velocidade+1
        
        if jogador.picareta_ativa==True:
            if jogador.picareta.colliderect(pedra.rect):
                    pedra.quebrar(jogador)
        
        if jogador.restaurar_ativa==True:
            if jogador.picareta.colliderect(pedra.rect):
                    pedra.restaurar(jogador)
        
        if oponente.picareta_ativa==True:
            if oponente.picareta.colliderect(pedra.rect):
                    pedra.quebrar(oponente)
        
        if oponente.restaurar_ativa==True:
            if oponente.picareta.colliderect(pedra.rect):
                    pedra.restaurar(oponente)
    
    tela.blit(Placar_esquerdo,(0,655))
    tela.blit(Placar_direito,(360,655))
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()
    
    pygame.display.update()
