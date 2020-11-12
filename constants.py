import pygame
import os
pygame.font.init()

# Tamanho da janela
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Vetor para os 3 tipos diferentes de imagem "bird"
BIRD_IMGS = [
    # Comando abaixo faz as imagens terem o dobro de tamanho
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),

    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),

    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]

# Imagem do cano
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

# Imagem do terreno mais baixo
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

# Imagem do plano de fundo
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
