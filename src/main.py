#import pygame
#from pygame.locals import *
#from sys import exit

#pygame.init()

largura=640
altura=480
tela=pygame.display.set_mode((largura, altura))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASSES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Pedra:
    def __init__(self,x_pedra,y_pedra):
        self.durabilidade=4
        self.x=x_pedra
        self.y=y_pedra
        self.cor=(70,70,70)
        self.rect=pygame.draw.rect(tela,(70,70,70),(x_pedra,y_pedra,50,50))
    
    def mostrar(self):
        self.rect=pygame.draw.rect(tela,self.cor,(self.x,self.y,50,50))
    
    def quebrar (self):
        self.durabilidade-=1
        print(self.durabilidade)
        if self.durabilidade==0:
            rect_pedras.remove(self)

class Personagem:
    def __init__(self,x_personagem,y_personagem):
        self.x=x_personagem
        self.y=y_personagem
        self.picareta=""
        self.x_picareta=0
        self.y_picareta=0
        self.pic_size=0
        self.facing="up"
        self.rect=""
    def mostrar(self):
        self.rect=pygame.draw.rect(tela, (255,0,0), (self.x,self.y,40,50))
    def minerar(self):
        
        self.pic_size=20
        
        if self.facing=="up":
            self.x_picareta=self.x+20
            self.y_picareta=self.y-20
            self.pic_size=1
        
        if self.facing=="down":
            self.x_picareta=self.x+20
            self.y_picareta=self.y+50
            self.pic_size=1
        
        if self.facing=="left":
            self.x_picareta=self.x-20
            self.y_picareta=self.y+25
        
        if self.facing=="right":
            self.x_picareta=self.x+40
            self.y_picareta=self.y+25
        
        #desenhar a picareta
        self.picareta=pygame.draw.rect(tela,(0,255,0),(self.x_picareta,self.y_picareta,self.pic_size,21-self.pic_size))
        
        for pedras in rect_pedras:
            if self.picareta.colliderect(pedras.rect):
                print("colidiu picareta")
                pedras.quebrar()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ JOGO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

jogador = Personagem(40,70)
rect_pedras=[Pedra(400,310),Pedra(120,110),Pedra(360,90),Pedra(510,240)]

# <<<outras variáveis>>>
velocidade=3




relogio = pygame.time.Clock()

while True:
    relogio.tick(60)
    tela.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        if event.type==KEYDOWN:
            if event.key==K_m:
                jogador.minerar() #colocar o método de minerar
    
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
    
    if jogador.y<0:
        jogador.y=0
    if jogador.y>(altura-50):
        jogador.y=altura-50
    if jogador.x<0:
        jogador.x=0
    if jogador.x>(largura-40):
        jogador.x=largura-40
    
    
    jogador.mostrar()
    
    
    for pedra in rect_pedras:
        pedra.mostrar()
    
    for pedra in rect_pedras:
        if jogador.rect.colliderect(pedra.rect):
            if pygame.key.get_pressed()[K_a]:
                jogador.x += velocidade*2
            if pygame.key.get_pressed()[K_d]:
                jogador.x -= velocidade*2
            if pygame.key.get_pressed()[K_s]:
                jogador.y -= velocidade*2
            if pygame.key.get_pressed()[K_w]:
                jogador.y += velocidade*2
            print("colidiu")
    
    
    
    pygame.display.update()
