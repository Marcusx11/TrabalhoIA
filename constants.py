import pygame
import os
pygame.font.init()

# Tamanho da janela
WIN_WIDTH = 500
WIN_HEIGHT = 800


# Imagem do cano
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))

# Imagem do terreno mais baixo
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

# Imagem do plano de fundo
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
