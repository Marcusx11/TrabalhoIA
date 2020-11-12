import pygame
import constants
import random


# Classe do cano do jogo
class Pipe:
    def __init__(self, x):
        self.GAP = 200
        self.VEL = 5  # Valor de velocidade que o canal se move pela tela

        self.x = x

        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(constants.PIPE_IMG, False, True)  # Cano na parte de cima
        self.PIPE_BOTTOM = constants.PIPE_IMG  # Cano na parte de baixo

        self.passed = False  # Verifica se o pássaro passou do cano ou não

        # Método abaixo vai definir o topo e a parte de baixo do canal e o seu tamanho total de altura
        # Será definido estes parâmetros aleatóriamente
        self.set_height()

    # Define os parametros do cano
    def set_height(self):
        self.height = random.randrange(50, 450)

        # Gerando os parâmetros para os canos que ficam em cima
        self.top = self.height - self.PIPE_TOP.get_height()

        # Gerando os parâmetros para os canos que ficam em baixo
        self.bottom = self.height + self.GAP

    # Movendo os canos ao decorrer do jogo
    def move(self):
        self.x -= self.VEL  # Movendo o cano para a direita

    # Desenha o cano na tela do jogo
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # Máscaras são como um array de pixels dentro de uma hitbox indicando o real conjunto de pixels do objeto
    # Elas auxiliam muito no processo de colisões, uma vez que permite uma melhor exatidão delas
    def collide(self, bird):
        bird_mask = bird.get_mask()

        # Pegando as máscaras dos canos
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Offset = Indica a distancia entre 2 máscaras
        top_offset = (self.x - bird.x, self.top - round(bird.y))  # Offset do pássaro para o cano superior
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))  # Offset do pássaro para o cano inferior

        # Verificando se as máscaras se colidem
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)  # Retorna None se não houve colisão
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True  # Indicando colisão com o pássaro de algum dos canos

        return False
