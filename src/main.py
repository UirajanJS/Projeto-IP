import pygame
from pygame.locals import *
from sys import exit

pygame.init()

largura=680
altura=680
tela=pygame.display.set_mode((largura, altura))

fonte = pygame.font.SysFont("arial",15,True,False)

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
            rect_pedras[-1].definir()
            

def espelhar():
    for y in range(16):
        for x in range(8):
            mapa[y][-x-1]=mapa[y][x]


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
        self.image=pygame.image.load("OneDrive\Documentos\Sprites\minerio_magnetita.png")
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
        self.image=pygame.image.load("OneDrive\Documentos\Sprites\minerio_cobre.png")
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
        self.image=pygame.image.load("OneDrive\Documentos\Sprites\minerio_ouro.png")
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
        self.image=pygame.image.load("OneDrive\Documentos\Sprites\muro.png")
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
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ JOGO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

jogador = Personagem(0,610)

oponente = Personagem(650,610)

todas_as_sprites = pygame.sprite.Group()

mapa=[
[12,O,12,22,M,N,12,12,X,N,N,N,N,N,N,N,N],
[M,25,12,N,N,12,C,25,N,N,N,N,N,N,N,N,N],
[25,N,20,12,N,12,20,12,X,N,N,N,N,N,N,N,N],
[N,N,C,25,22,12,O,N,X,N,N,N,N,N,N,N,N],
[N,12,N,N,12,12,20,M,X,N,N,N,N,N,N,N,N],
[15,12,15,12,12,22,N,12,X,N,N,N,N,N,N,N,N],
[M,22,12,22,C,12,N,25,N,N,N,N,N,N,N,N,N],
[N,25,O,12,12,20,22,C,X,N,N,N,N,N,N,N,N],
[22,10,22,N,N,12,12,N,X,N,N,N,N,N,N,N,N],
[22,C,12,22,12,20,M,20,X,N,N,N,N,N,N,N,N],
[12,22,N,N,20,12,22,12,X,N,N,N,N,N,N,N,N],
[M,12,12,C,12,20,22,C,X,N,N,N,N,N,N,N,N],
[12,20,N,12,20,N,12,12,X,N,N,N,N,N,N,N,N],
[20,N,20,N,12,C,20,31,N,N,N,N,N,N,N,N,N],
[N,N,N,12,22,20,N,12,X,N,N,N,N,N,N,N,N],
[N,N,N,20,C,12,20,M,X,N,N,N,N,N,N,N,N]]

rect_pedras=[]

espelhar()
mapear()

# <<<outras variáveis>>>
velocidade=5


relogio = pygame.time.Clock()

while True:
    #                          Setup de variáveis
    relogio.tick(30)
    tela.fill((0,0,0))
    jogador.picareta_ativa=False
    jogador.restaurar_ativa=False
    oponente.picareta_ativa=False
    oponente.restaurar_ativa=False
    items_jogador=f"Magnetita: {jogador.items["Magnetita"]} | Cobre: {jogador.items["Cobre"]} | Ouro: {jogador.items["Ouro"]} | Pedras {jogador.items["Pedra"]}"
    Placar_esquerdo = fonte.render(items_jogador, False, (255,255,255))
    items_oponente=f"Magnetita: {oponente.items["Magnetita"]} | Cobre: {oponente.items["Cobre"]} | Ouro: {oponente.items["Ouro"]} | Pedra: {oponente.items["Pedra"]}"
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
    if jogador.y>(altura-y_jog-30):
        jogador.y=altura-y_jog-30
    if jogador.x<0:
        jogador.x=0
    if jogador.x>(largura-x_jog):
        jogador.x=largura-x_jog
    
    if oponente.y<0:
        oponente.y=0
    if oponente.y>(altura-y_jog-30):
        oponente.y=altura-y_jog-30
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
    
    tela.blit(Placar_esquerdo,(0,648))
    tela.blit(Placar_direito,(360,648))
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()
    
    pygame.display.update()
