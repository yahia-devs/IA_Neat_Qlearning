import pickle
from game import Game



def discretiser_distance(dx):
    if dx < 0:
        return "passe"
    elif dx < 5:
        return "tres_proche"
    elif dx < 50:
        return "proche"
    elif dx < 75:
        return "moyen"
    elif dx < 100:
        return "loin"
    else:
        return "tres_loin"


def discretiser_hauteur(posY, posA, taille):
    sol = posA - taille
    if posY < sol - taille * 0.5:
        return "haut"
    elif posY < sol - 5:
        return "saut"
    else:
        return "sol"


def discretiser_etat(state, game):
    dx, dy, dx2, dy2, posY, obstacle_haut , meme_pose = state

    dist1 = discretiser_distance(dx)
    hauteur = discretiser_hauteur(posY, game.posA, game.taille_cube)
    type1 = "haut" if obstacle_haut == 1 else "bas"

    if dx2 < 9000:
        dist2 = discretiser_distance(dx2)
        sol = game.posA - game.taille_cube
        type2 = "haut" if dy2 != sol else "bas"
    else:
        dist2 = type2 = "aucun"

    return (dist1, type1, hauteur, dist2, type2 , meme_pose)



Q = pickle.load(open("qtable.pkl","rb"))

class AIPlayer:
    def choose(self, state):
        q0 = Q.get((state,0),0)
        q1 = Q.get((state,1),0)
        return 1 if q1 > q0 else 0


def play():
    import pygame
    game = Game(use_pygame=True)
    ai = AIPlayer()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        if game.running:
            s = discretiser_etat(game.get_state(), game)
            action = ai.choose(s)
            game.update(action)
            game.draw()
            game.clock.tick(60)
        else:
            game.reset()


play()
