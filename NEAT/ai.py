import neat
import pickle
import pygame
from game import Game

RENDER = False


def discretiser_distance(dx):
    if dx < 0:
        return 0
    elif dx < 20:
        return 1
    elif dx < 50:
        return 2
    elif dx < 100:
        return 3
    elif dx < 200:
        return 4
    else:
        return 5


def discretiser_hauteur(y, posA, taille):
    sol = posA - taille
    if y < sol - taille * 0.5:
        return 2
    elif y < sol - 5:
        return 1
    else:
        return 0


def obtenir_inputs_discrets(game):
    dx, dy, dx2, dy2, posY, obs_haut = game.get_state()

    dist1 = discretiser_distance(dx)
    hauteur_joueur = discretiser_hauteur(posY, game.posA, game.taille_cube)
    type1 = 1 if obs_haut == 1 else 0

    if dx2 < 9000:
        dist2 = discretiser_distance(dx2)
        sol = game.posA - game.taille_cube
        type2 = 1 if dy2 != sol else 0
    else:
        dist2 = 5
        type2 = 0

    return (dist1, type1, hauteur_joueur, dist2, type2)


def verifier_passage(game, anciens_obs):
    passes = 0
    for i, obs in enumerate(game.obstacles):
        ancien_x = anciens_obs[i][0]
        nouveau_x = obs[0]
        if ancien_x + game.taille_obstacle > game.posX and nouveau_x + game.taille_obstacle <= game.posX:
            passes += 1
    return passes


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0.0
        game = Game()
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        frame_count = 0
        max_frames = 1000

        while game.running and frame_count < max_frames:
            frame_count += 1

            anciens_obs = [o.copy() for o in game.obstacles]
            inputs = obtenir_inputs_discrets(game)

            output = net.activate(inputs)
            action = 1 if output[0] > 0.5 else 0

            game.update(action)

            if RENDER:
                game.draw()
                game.clock.tick(60)

            genome.fitness += 1.0

            passes = verifier_passage(game, anciens_obs)
            if passes > 0:
                genome.fitness += 50.0 * passes

            dist1, type1, _, _, _ = inputs
            if action == 1 and dist1 in [4, 5]:
                genome.fitness -= 2.0

            if not game.running:
                genome.fitness -= 100.0
                break

        if genome.fitness < 0:
            genome.fitness = 0


def run():
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "config.txt"
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    winner = pop.run(eval_genomes, 30)

    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)

    print("\n train termine.")
    #print("Meilleur cerveau sauvegardé dans winner.pkl\n")


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

        inputs = obtenir_inputs_discrets(game)
        output = net.activate(inputs)
        action = 1 if output[0] > 0.5 else 0

        game.update(action)
        game.draw()
        game.clock.tick(60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "play":
        play_with_best()
    else:
        run()