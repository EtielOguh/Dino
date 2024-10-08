import pygame
from pygame.locals import*
from sys import exit
import os
from random import randrange, choice

pygame.init()
pygame.mixer.init()

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

LARGURA = 640
ALTURA = 480

BRANCO = (255,255,255)
PRETO = (0,0,0)

tela = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption('Jogo Dino')

sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens,'dinoSpritesheet.png')).convert_alpha()
#O convert alpah se a imagem tiver transparencia ele realmente fica transparente, ignora

som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'score_sound.wav'))
som_pontuacao.set_volume(1)

escolha_obstaculo = choice ([0,1,2])

pontos = 0
velocidade_jogo = 15


def exibe_mensagem(msg, tamanho, cor):
    fonte = pygame.font.SysFont('timesnewroman', tamanho, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor)
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, escolha_obstaculo
    pontos = 0
    velocidade_jogo = 15
    dino.rect.y = ALTURA - 56 - 64//2
    dino.pulo = False
    dino_voador.rect.x = LARGURA
    dino_voador2.rect.x = LARGURA
    cacto.rect.x = LARGURA
    escolha_obstaculo = choice([0,1,2])


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32,0), (32,32))
            img= pygame.transform.scale(img,(32*2, 32*2))
            self.imagens_dinossauro.append(img)
        
        self.indexlista = 0
        self.image = self.imagens_dinossauro[self.indexlista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) #Criando a mascara da Sprite
        self.pos_y_inicial = ALTURA - 56 - 64//2
        self.rect.center = (100,ALTURA-56)
        self.pulo = False
    
    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo == True:
            if self.rect.y <= 330:
                self.pulo = False
            self.rect.y -= 15
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 10
            else:
                self.rect.y = self.pos_y_inicial


        if self.indexlista > 2:
            self.indexlista = 0
        self.indexlista += 0.25
        self.image = self.imagens_dinossauro[int(self.indexlista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*3, 32*3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(0,150, 50) #um numero entre 50 e 200 pulando de x em x
        self.rect.x = LARGURA - randrange(30, 300, 90)
        #self.rect.center = (100,100)
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.y = randrange(0,150, 50)
            self.rect.x = LARGURA
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect()
        self.rect.y = ALTURA - 64
        self.rect.x = pos_x * 64
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = LARGURA
        self.rect.x -= 10

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5*32, 0), (32,32))
        self.image = pygame.transform.scale(self.image, (32*2, 32*2))
        self.rect = self.image.get_rect() #Pega o retangulo da imagem
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect.center = (LARGURA, ALTURA - 64)#x, y
        self.rect.x = LARGURA

    def update(self):
        if self.escolha == 0:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

class DinoVoador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0),(32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 300) #Colocar na tela
        self.rect.x = LARGURA
        self.rect.y = 300
    
    def update(self):
        if self.escolha == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.15
            self.image = self.imagens_dinossauro[int(self.index_lista)]

class DinoVoador2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_dinossauro = []
        for i in range(3,5):
            img = sprite_sheet.subsurface((i*32, 0),(32, 32))
            img = pygame.transform.scale(img, (32*3, 32*3))
            self.imagens_dinossauro.append(img)

        self.index_lista = 0
        self.image = self.imagens_dinossauro[self.index_lista]
        self.mask = pygame.mask.from_surface(self.image)
        self.escolha = escolha_obstaculo
        self.rect = self.image.get_rect()
        self.rect.center = (LARGURA, 420) #Colocar na tela
        self.rect.x = LARGURA
    
    def update(self):
        if self.escolha == 2:
            if self.rect.topright[0] < 0:
                self.rect.x = LARGURA
            self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.15
            self.image = self.imagens_dinossauro[int(self.index_lista)]
    
todas_as_sprites = pygame.sprite.Group()
dino = Dino()
todas_as_sprites.add(dino)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)

for i in range(640*2//64):
    chao = Chao(i)
    todas_as_sprites.add(chao)

cacto = Cacto()
todas_as_sprites.add(cacto)

dino_voador = DinoVoador()
todas_as_sprites.add(dino_voador)

dino_voador2 = DinoVoador2()
todas_as_sprites.add(dino_voador2)

grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(cacto)
grupo_obstaculos.add(dino_voador)
grupo_obstaculos.add(dino_voador2)

relogio = pygame.time.Clock()

while True:
    relogio.tick(25)
    tela.fill(BRANCO)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()

            if event.key == K_r and colisoes:
                reiniciar_jogo()

    
    colisoes = pygame.sprite.spritecollide(dino, grupo_obstaculos, False, pygame.sprite.collide_mask) #Analisar
    
    todas_as_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or dino_voador.rect.topright[0] <= 0 or dino_voador2.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0,1,2])
        cacto.rect.x = LARGURA
        dino_voador.rect.x = LARGURA
        dino_voador2.rect.x = LARGURA
        cacto.escolha = escolha_obstaculo
        dino_voador.escolha = escolha_obstaculo
        dino_voador2.escolha = escolha_obstaculo

    if colisoes:
        game_over = exibe_mensagem('GAME OVER', 40, PRETO)
        tela.blit(game_over, (LARGURA//3.3, ALTURA//3))
        reiniciar = exibe_mensagem('Pressione R para reiniciar', 20, PRETO)
        tela.blit(reiniciar,(LARGURA//3.1, ALTURA//2.3))


    else:
        pontos += 1
        todas_as_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, PRETO)
    
    if pontos % 100 == 0:
        if colisoes:
            pass
        som_pontuacao.play()
        if velocidade_jogo >= 100:
            velocidade_jogo += 0
        else:
            velocidade_jogo += 1

        print(velocidade_jogo)

    tela.blit(texto_pontos, (520, 30))


    pygame.display.flip()