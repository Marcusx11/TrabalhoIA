# Módulos baixados
import constants
import pygame
from game_objects.bird import Bird
from game_objects.pipe import Pipe
from game_objects.base import Base
import os
import neat

# Número de gerações
GEN = 0


# Desenha a janela de fundo do jogo com o objeto do pássaro
def draw_window(window, bird, pipes, base, score, gen):
    window.blit(constants.BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(window)

    text = constants.STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    window.blit(text, (constants.WIN_WIDTH - 10 - text.get_width(), 10))  # Faz o texto acompanhar a tela

    # Geração atual
    gen = constants.STAT_FONT.render("Geração: " + str(gen), 1, (255, 255, 255))
    window.blit(gen, (10, 10))

    base.draw(window)

    for bird in bird:
        bird.draw(window)

    # Dá uma refresh na tela para atualizar as modificações nas imagens
    pygame.display.update()


# Função "fitness" da rede
def main(genomes, config):
    # Número da gerações
    global GEN
    GEN += 1

    # Array de redes neurais dos pássaros
    nets = []
    # Array de genótipos
    ge = []
    # Arrays de objetos de pássaro
    birds = list()

    # Setando uma rede neural para os genótipos
    for _, g in genomes:
        # Adicionando uma nova rede
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)  # Fundo da tela do jogo
    pipes = [Pipe(600)]

    win = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))

    clock = pygame.time.Clock()

    game_run = True

    score = 0  # Pontuação do jogo

    # Loop principal do jogo
    while game_run:

        clock.tick(30)

        # Mantém um olho em eventos do usuário na execução do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
                quit()
                break

        pipe_ind = 0
        if len(birds) > 0:
            # Pegando-se o primeiro pássaro arbitráriamente
            if len(pipes) > 0 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

        else:
            game_run = False
            # Parar esta geração (encerrar o jogo)
            break

        # Passando valores para a rede neural associada com o passaro para ele pular dos canos
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1

            # Output é uma lista
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),
                                       abs(bird.y - pipes[pipe_ind].bottom)))

            # Verificando a saída para fazer o pássaro pular
            if output[0] > 0.5:
                bird.jump()

        # Lista dos canos removidos
        rem_pipes = []
        add_pipe = False  # Controle de mostrar um novo cano ou não

        # Movendo os ojbetos do jogo
        # bird.move()
        base.move()
        for pipe in pipes:
            for x, bird in enumerate(birds):  # Pegando-se a posição na lista
                # Verifica colisão dos pássaros
                if pipe.collide(bird):
                    # Pássaros que colidem com os canos tem seu fitness subtraído em 1
                    # Ajuda na garantia de selecionar os indivíduos que mais forem longe no jogo
                    ge[x].fitness -= 1
                    # Removendo os pássaros que colidem da rede
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # Checa se o pássaro passou dos canos
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Checa se o cano está completamente fora de cena
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem_pipes.append(pipe)  # Removendo os canos

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                # Aumentando em 5 o fitness para "incentivar" os pássaros e irem mais longe
                g.fitness += 5
            pipes.append(Pipe(600))

        # Removendo os canos fora de cena
        for rem in rem_pipes:
            pipes.remove(rem)

        for x, bird in enumerate(birds):
            # Pássaro caiu no chão:
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        # Mostra os elementos do jogo na tela
        draw_window(win, birds, pipes, base, score, GEN)


def run(configpath):
    # Setando propriedades da biblioteca neat a partir do arquivo texto de configuração
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, configpath)

    # Definindo a população de pássaros
    population = neat.Population(config)

    # Output do algoritmo
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()  # Status do algoritmo
    population.add_reporter(stats)

    # Executa a função "main()" 50 vezes passando os parametros da população
    winner = population.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    run(config_path)
