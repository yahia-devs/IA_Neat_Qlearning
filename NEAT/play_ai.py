import neat
import pickle
import pygame
from game import Game


def play_with_best():
    pygame.init()

    with open("winner.pkl", "rb") as f:
        winner = pickle.load(f)

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt"
    )

    net = neat.nn.FeedForwardNetwork.create(winner, config)

    game = Game()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if not game.running:
            game.show_game_over()
            continue

        dx, dy, dx2, dy2, posY , obstacle_haut = game.get_state()

        output = net.activate(( dx, dy, dx2, dy2, posY , obstacle_haut ))
        action = 1 if output[0] > 0.5 else 0

        game.update(action)
        game.draw()
        game.clock.tick(60)  



if __name__ == "__main__":
    play_with_best()
