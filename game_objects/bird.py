import constants
import pygame


class Bird:
    def __init__(self, x, y):
        self.IMGS = constants.BIRD_IMGS
        self.MAX_ROTATION = 25  # Rotação máxima do pássaro
        self.ROT_VEL = 20  # Velocidade de rotação
        self.ANIMATION_TIME = 5  # O tempo de amostra da animação do pássaro

        # Posição inicial do pássaro
        self.x = x
        self.y = y

        # Inclinação da imagem do pássaro
        self.tilt = 0

        self.tick_count = 0
        self.vel = 0  # Velocidade do pássaro

        self.height = self.y
        self.img_count = 0  # Qual imagem está mostrando atualmente do vetor

        # Imagem inicial do pássaro:
        self.img = self.IMGS[0]

    # Método para fazer o pássaro pular
    def jump(self):
        self.vel = -10.5

        self.tick_count = 0  # Contagem para manter o controle de quando foi o último pulo

        self.height = self.y

    # Método para mover o pássaro pelos frames
    def move(self):
        self.tick_count += 1

        # Deslocamento de pixels para cima/baixo e direita/esquerda
        # Equação física do movimento do pássaro (equação do 2 grau)
        # tick_count é como o tempo na equação
        # Realiza um movimento de pulo em uma forma de parábola
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        # Ponto em que o pássaro não acelera mais
        if displacement >= 16:
            displacement = 16

        # Faz os pulos serem um pouco mais altos
        if displacement < 0:
            displacement -= 2

        # Pulo do pássaro
        self.y = self.y + displacement

        # ------------ Trecho para tratar a inclinação do pássaro ------------ #
        if displacement < 0 or self.y < self.height + 50:
            # Inclina o pássaro para cima
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        else:
            # Inclina o pássaro para baixo
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    # Exibe o pássaro na tela
    def draw(self, window):
        # Contagem de quantas vezes a imagem foi mostrada no jogo
        self.img_count += 1

        # Mudanças na animação de movimento do pássaro
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotacionar uma imagem a partir de seu centro
        # Tilt é como o angulo de rotação da imagem
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        # Mostra o pássaro na tela do jogo
        window.blit(rotated_img, new_rect.topleft)

    # Auxílio nas colisões de objetos
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

