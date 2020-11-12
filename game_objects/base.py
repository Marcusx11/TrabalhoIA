import pygame
import constants


# Classe do chão
class Base:
    def __init__(self, y):
        self.VEL = 5
        self.WIDTH = constants.BASE_IMG.get_width()
        self.IMG = constants.BASE_IMG

        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    # Mover-se o terreno base
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Causando "ilusão" de movimento contínuo
        """ Move-se duas imagens simultaneamente para a esquerda.
            Quando a imagem mais a esquerda sair de tela, ela será
            reposicionada para a direita após a segunda imagem e assim,
            sucessivamente..."""
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    # Desenha o terreno de chão na tela
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
