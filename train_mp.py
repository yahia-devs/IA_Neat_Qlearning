import random
from game import Game

ALPHA = 0.1
GAMMA = 0.85
EPSILON_DEBUT = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.9995

RECOMPENSE_VIE = 1.0
RECOMPENSE_OBSTACLE = 50.0
PENALITE_MORT = -100.0
PENALITE_SAUT = -2.0

NB_EPISODES = 500000


class JeuSimulation:
    def __init__(self):
        self.dimX = 1200
        self.dimY = 1000
        self.taille_cube = 60
        self.taille_obstacle = 60
        self.posA = self.dimY - 300
        self.gravite = 1
        self.force_saut = -20
        self.vitesse = 5
        self.nb_obstacles = 4
        self.reinitialiser()

    def reinitialiser(self):
        self.posX = 50
        self.posY = self.posA - self.taille_cube
        self.velocityY = 0
        self.score = 0
        self.running = True
        self.obstacles = []
        for i in range(self.nb_obstacles):
            x = random.randint(self.dimX + i * 300, self.dimX + i * 600)
            y = random.choice([self.posA - self.taille_cube, self.posA - self.taille_cube * 2])
            self.obstacles.append([x, y])

    def get_state(self):
        obs = [o for o in self.obstacles if o[0] >= self.posX]
        obs.sort(key=lambda o: o[0])

        dx = obs[0][0] - self.posX
        dy = obs[0][1]
        obs_haut = 1 if dy != self.posA - self.taille_cube else 0

        if len(obs) > 1:
            dx2 = obs[1][0] - self.posX
            dy2 = obs[1][1]
        else:
            dx2 = dy2 = 9999

        return (dx, dy, dx2, dy2, self.posY, obs_haut)

    def update(self, action):
        if action == 1 and self.posY == self.posA - self.taille_cube:
            self.velocityY = self.force_saut

        self.velocityY += self.gravite
        self.posY += self.velocityY

        if self.posY >= self.posA - self.taille_cube:
            self.posY = self.posA - self.taille_cube
            self.velocityY = 0

        for obs in self.obstacles:
            obs[0] -= self.vitesse
            if obs[0] < -self.taille_obstacle:
                obs[0] = random.randint(self.dimX, self.dimX + 550)
                obs[1] = random.choice([self.posA - self.taille_cube, self.posA - self.taille_cube * 2])

        for ox, oy in self.obstacles:
            if (self.posX < ox + self.taille_obstacle and
                    self.posX + self.taille_cube > ox and
                    self.posY < oy + self.taille_obstacle and
                    self.posY + self.taille_cube > oy):
                self.running = False
                return

        self.score += 1


def discretiser_distance(dx):
    if dx < 0:
        return "passe"
    elif dx < 1:
        return "tres_proche"
    elif dx < 100:
        return "proche"
    elif dx < 200:
        return "moyen"
    elif dx < 300:
        return "loin"
    else:
        return "tres_loin"


def discretiser_hauteur(y, posA, taille):
    sol = posA - taille
    if y < sol - taille * 0.5:
        return "haut"
    elif y < sol - 5:
        return "saut"
    else:
        return "sol"


def obtenir_etat_discret(jeu):
    dx, dy, dx2, dy2, posY, obs_haut = jeu.get_state()

    dist1 = discretiser_distance(dx)
    hauteur = discretiser_hauteur(posY, jeu.posA, jeu.taille_cube)
    type1 = "haut" if obs_haut == 1 else "bas"

    if dx2 < 9000:
        dist2 = discretiser_distance(dx2)
        sol = jeu.posA - jeu.taille_cube
        type2 = "haut" if dy2 != sol else "bas"
    else:
        dist2 = type2 = "aucun"

    return (dist1, type1, hauteur, dist2, type2)


def verifier_passage(jeu, anciens_obs):
    passes = []
    for i, obs in enumerate(jeu.obstacles):
        ancien_x = anciens_obs[i][0]
        nouveau_x = obs[0]
        if ancien_x + jeu.taille_obstacle > jeu.posX and nouveau_x + jeu.taille_obstacle <= jeu.posX:
            passes.append(i)
    return passes


def calculer_recompense(jeu, action, passes):
    recompense = RECOMPENSE_VIE
    if passes:
        recompense += RECOMPENSE_OBSTACLE * len(passes)
    d1, _, _, _, _ = obtenir_etat_discret(jeu)
    if action == 1 and d1  in  ["proche" , "moyen","loin"]:
        recompense += PENALITE_SAUT
    if not jeu.running:
        recompense += PENALITE_MORT
    return recompense


def choisir_action(etat, Q, epsilon):
    if random.random() < epsilon:
        return random.choice([0, 1])
    q0 = Q.get((etat, 0), 0.0)
    q1 = Q.get((etat, 1), 0.0)
    return 1 if q1 > q0 else 0


def mettre_a_jour_q(Q, etat, action, recompense, etat_suivant):
    ancien_q = Q.get((etat, action), 0.0)
    meilleur_q = max(Q.get((etat_suivant, a), 0.0) for a in [0, 1])
    Q[(etat, action)] = ancien_q + ALPHA * (recompense + GAMMA * meilleur_q - ancien_q)


def entrainer():
    Q = {}
    epsilon = EPSILON_DEBUT
    meilleur = 0

    print("train sur ",NB_EPISODES," episode")

    for ep in range(1, NB_EPISODES + 1):
        jeu = JeuSimulation()
        etat = obtenir_etat_discret(jeu)

        while jeu.running:
            anciens_obs = [o.copy() for o in jeu.obstacles]
            action = choisir_action(etat, Q, epsilon)
            jeu.update(action)
            etat_suivant = obtenir_etat_discret(jeu)
            passes = verifier_passage(jeu, anciens_obs)
            recompense = calculer_recompense(jeu, action, passes)
            mettre_a_jour_q(Q, etat, action, recompense, etat_suivant)
            etat = etat_suivant

        epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)
        if jeu.score > meilleur:
            meilleur = jeu.score

        if ep % 100 == 0:
            print("Ep ",ep ," | Score: ",jeu.score ,"  | Meilleur: ",meilleur ,"")

    return Q


def tester(Q):

    import pygame
    pygame.init()
    jeu = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return

        if jeu.running:
            etat = obtenir_etat_discret(jeu)
            q0 = Q.get((etat, 0), 0.0)
            q1 = Q.get((etat, 1), 0.0)
            action = 1 if q1 > q0 else 0
            jeu.update(action)
            jeu.draw()
        else:
            texte = jeu.font.render("GAME OVER - Score: ",int(jeu.score) , ", True, (255, 0, 0)")
            jeu.screen.blit(texte, (jeu.dimX // 2 - 250, jeu.dimY // 2))
            texte2 = jeu.font.render("ESPACE = Rejoue  ou  ESC = Quitter", True, (255, 255, 255))
            jeu.screen.blit(texte2, (jeu.dimX // 2 - 250, jeu.dimY // 2 + 60))
            pygame.display.update()

            touches = pygame.key.get_pressed()
            if touches[pygame.K_SPACE]:
                jeu.reset()
            if touches[pygame.K_ESCAPE]:
                pygame.quit()
                return

        jeu.clock.tick(60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        tester()
    else:
        Q = entrainer()
        if input("Tester? (o/n): ").lower() == 'o':
            tester(Q)