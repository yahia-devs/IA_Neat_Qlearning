
import random
import pygame
from game import Game



Q = {}







ALPHA = 0.2
GAMMA = 0.9
EPSILONE = 1.

eta_epsilone = 0.995935335455343535464646



RECOMPENSE = 10



BONUS_SURVIE = 0.1
BONUS_OBSTACLE = 50
MALUS_SAUT_INUTILE = -1
MALUS_MORT = -5

episode = 2000


def discret_to_continue (valeur , tranche ):
    return int (valeur // tranche )


def etat (game ):
    dx, dy, dx2, dy2, posY , obstacle_haut = game.get_state()
    # dx = discret_to_continue(dx , 50 )
    # dy = discret_to_continue(dy , 50)
    # dx2 = discret_to_continue(dx2 , 50)
    # dy2 = discret_to_continue(dy2,50)
    return  dx, dy, dx2, dy2, posY , obstacle_haut



def choisir_action (etat):
    if random.random() < EPSILONE :
        return random.choice([0 ,1])
    else :
        q_saut = Q.get((etat , 1), 0  )
        q_rien = Q.get((etat ,0 ), 0 )
    return 1 if q_saut > q_rien else 0



def calculer_recompense ( game , action , etats , new_etat ):
    dx, dy, dx2, dy2, posY, obstacle_haut = etats

    recompense = BONUS_SURVIE

    if action == 1 and obstacle_haut == 1 :
        recompense += MALUS_SAUT_INUTILE
    if action == 1 and obstacle_haut == 0 :
        recompense += BONUS_OBSTACLE
    if not game.running:
        recompense += MALUS_MORT
    if dx < 5 and obstacle_haut == 0 :
        recompense += BONUS_OBSTACLE
    if dx < 5 and obstacle_haut == 1 and posY >= posY - 60:
        recompense += MALUS_SAUT_INUTILE



    return recompense



def train():
    global EPSILONE

    for i in range(episode):
        game = Game()
        etats = etat(game)

        while game.running:
            action = choisir_action(etats)
            game.update(action)
            new_etat = etat(game)
            recompense = calculer_recompense(game, action, etats, new_etat)

            if (etats, action) not in Q:
                Q[(etats, action)] = 0

            ancien_q = Q.get((etats, action), 0)
            meilleur_futur_q = max(Q.get((new_etat, a), 0) for a in [0, 1])

            Q[(etats, action)] = ancien_q + ALPHA * (recompense + GAMMA * meilleur_futur_q - ancien_q)

            etats = new_etat

        EPSILONE *= eta_epsilone
        print("Épisode " , i +1 ,",/" , episode , "termine epsilon= " , EPSILONE )





train()
pygame.quit()



def test ():
    pygame.init()


    game = Game()
    EPSILONE = 0


    while game.running:

        etats = etat(game)

        action= max ([0 ,1] , key = lambda  a : Q.get((etats , a ) ,0)  )


        game.update(action)

        game.draw()
        game.clock.tick(60)

test()


