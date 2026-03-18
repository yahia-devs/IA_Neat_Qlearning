from game import Game
import random
import pickle

ALPHA = 0.1
GAMMA = 0.85
EPSILON = 1.0
EPSILON_GAP = 0.9995
EPSILON_MIN = 0.01

REWARD_STEP = 1
REWARD_PASS = 50
REWARD_DEATH = -100
PENALTY_JUMP = -2

EPISODES = 20000



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



def choose_action(state, Q, eps):
    if random.random() < eps:
        return random.choice([0,1])
    return 1 if Q.get((state,1),0) > Q.get((state,0),0) else 0


def update_Q(Q, s, a, r, s2):
    old = Q.get((s,a), 0)
    best = max(Q.get((s2,0),0), Q.get((s2,1),0))
    Q[(s,a)] = old + ALPHA * (r + GAMMA*best - old)


def train():
    Q = {}
    epsilon = EPSILON


    best_score = 0
    for ep in range(1, EPISODES+1):
        env = Game(use_pygame=False)
        s = discretiser_etat(env.get_state(), env)

        while env.running:
            action = choose_action(s, Q, epsilon)

            old_obs = [o[0] for o in env.obstacles]

            env.update(action)

            #print(f"Score {env.score}")
            s2 = discretiser_etat(env.get_state(), env)

            reward = REWARD_STEP

            for i, (ox, oy) in enumerate(env.obstacles):
                if old_obs[i] >= env.posX and ox < env.posX:
                    reward += REWARD_PASS

            if action == 1 and s[0] in ["proche","moyen","loin","tres_loin"] :
                reward += PENALTY_JUMP
            if action == 1 and s[5] == 1:
                reward -= PENALTY_JUMP
            if action == 1 and s[0] in ["tres_proche"]:
                reward -= PENALTY_JUMP*4

            if not env.running:
                reward += REWARD_DEATH

            update_Q(Q, s, action, reward, s2)
            s = s2

            if env.score > 100000 :
                break

        epsilon = max(EPSILON_MIN, epsilon * EPSILON_GAP)


        if env.score > best_score :
            best_score = env.score
        if best_score > 100000 :
            break
        if ep % 200 == 0:
            print(f"Episode {ep} | Score {env.score} | Best scoore {best_score}")
        env.reset()

    pickle.dump(Q, open("qtable.pkl", "wb"))
    print("IA entraînée ! Q-table sauvegardée dans qtable.pkl")


train()
