import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura=680
altura=640
tela=pygame.display.set_mode((largura, altura))

#não fazer tamanhos ímpares, por causa da parte da picareta
x_jog=26
y_jog=26

size_pedra=40

#parametros
P="P"
M="M"
O="O"
C="C"
X="X"
N="N"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FUNÇÕES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def mapear():
    objeto=""
    for y in range(16):
        for x in range(17):
            objeto = mapa[y][x]
            if type(objeto)==int:
                rect_pedras.append(Pedra(x*40,y*40,objeto))
            elif objeto=="M":
                rect_pedras.append(Magnetita(x*40,y*40))
            elif objeto=="O":
                rect_pedras.append(Ouro(x*40,y*40))
            elif objeto=="C":
                rect_pedras.append(Cobre(x*40,y*40))
            elif objeto=="X":
                rect_pedras.append(Muro(x*40,y*40))
            elif objeto=="N":
                pass
            else:
                print("error")


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MINÉRIOS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Pedra:
    def __init__(self,x_pedra,y_pedra,durabilidade=1):
        #propriedades básicas
        self.durabilidade=durabilidade
        self.x=x_pedra
        self.y=y_pedra
        self.cor=(0,0,0)
        self.rect="" #objeto retângulo
    
    #desenhar a pedra na tela
    def mostrar (self):
        self.cor=(132-self.durabilidade*3,132-self.durabilidade*3,132-self.durabilidade*3)
        self.rect=pygame.draw.rect(tela,self.cor,(self.x,self.y,size_pedra,size_pedra))
    
    #função chamada para reduzir a durabilidade
    def quebrar (self, nome):
        self.durabilidade-=nome.dano_picareta
        if self.durabilidade<=0:
            nome.items["Pedra"]+=1
            rect_pedras.remove(self)
    def restaurar (self, nome):
        while (self.durabilidade<=31) and (nome.items["Pedra"]>0):
            self.durabilidade+=1
            nome.items["Pedra"]-=1

class Magnetita(Pedra):
    def mostrar (self):
        self.rect=pygame.draw.rect(tela,(128,0,128),(self.x,self.y,size_pedra,size_pedra))
    #função chamada para reduzir a durabilidade
    def quebrar (self,nome):
        nome.items["Magnetita"]+=1
        nome.dano_picareta=1+(nome.items["Magnetita"]//2) #☼☼☼☼☼☼☼
        rect_pedras.remove(self)
        print(nome.items)

class Cobre(Pedra):
    def mostrar (self):
        self.rect=pygame.draw.rect(tela,(206,137,70),(self.x,self.y,size_pedra,size_pedra))
    #função chamada para reduzir a durabilidade
    def quebrar (self,nome):
        nome.items["Cobre"]+=1
        rect_pedras.remove(self)
        print(nome.items)

class Ouro(Pedra):
    def mostrar (self):
        self.rect=pygame.draw.rect(tela,(255,215,0),(self.x,self.y,size_pedra,size_pedra))
    #função chamada para reduzir a durabilidade
    def quebrar (self,nome):
        nome.items["Ouro"]+=1
        rect_pedras.remove(self)
        print(nome.items)

class Muro (Pedra):
    def mostrar (self):
        self.rect=pygame.draw.rect(tela,(255,0,0),(self.x,self.y,size_pedra,size_pedra))
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ JOGO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

jogador = Personagem(0,610)
oponente = Personagem(650,610)

mapa=[
[M,N,X,N,N,N,N,N,N,N,N,N,N,N,N,N,20],
[M,N,X,N,N,N,N,N,N,N,N,N,N,N,N,N,20],
[M,N,X,N,N,N,N,N,N,N,N,N,N,N,N,N,20],
[M,N,X,N,N,N,N,N,N,N,N,N,N,N,N,N,20],
[M,N,X,X,X,X,N,N,N,N,N,N,N,N,N,N,20],
[M,N,N,N,N,N,N,N,N,N,N,N,N,O,N,N,N],
[M,N,N,N,N,N,N,N,N,N,N,N,N,O,N,N,N],
[M,N,N,N,N,N,N,N,N,N,N,N,O,O,N,N,N],
[M,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N,N],
[M,N,N,N,N,N,N,10,10,10,N,N,N,N,N,N,N],
[N,N,N,N,N,X,N,N,N,N,N,N,N,N,N,N,N],
[N,N,X,X,X,X,N,N,N,C,N,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,C,C,C,N,N,N,N,N,N],
[N,N,N,N,N,N,N,N,N,C,N,N,N,N,M,M,M],
[N,N,N,N,N,N,N,N,N,N,N,N,N,N,M,M,M],
[N,N,N,N,N,N,N,N,N,N,N,N,N,N,M,M,M]]

rect_pedras=[]

mapear()

# <<<outras variáveis>>>
velocidade=5


relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill((0,0,0))
    jogador.picareta_ativa=False
    jogador.restaurar_ativa=False
    oponente.picareta_ativa=False
    oponente.restaurar_ativa=False
    
    for event in pygame.event.get():
        if event.type==QUIT:
            print(jogador.items)
            print(oponente.items)
            print(rect_pedras)
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
    if jogador.y>(altura-y_jog):
        jogador.y=altura-y_jog
    if jogador.x<0:
        jogador.x=0
    if jogador.x>(largura-x_jog):
        jogador.x=largura-x_jog
    
    if oponente.y<0:
        oponente.y=0
    if oponente.y>(altura-y_jog):
        oponente.y=altura-y_jog
    if oponente.x<0:
        oponente.x=0
    if oponente.x>(largura-x_jog):
        oponente.x=largura-x_jog
    
    
    #                    mostrar objetos na tela
    jogador.mostrar()
    oponente.mostrar()
    for pedra in rect_pedras:
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

    
    
    pygame.display.update()
