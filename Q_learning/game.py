import random


import pygame
seed = 50
#random.seed(seed)


class Game:
    def __init__(self, use_pygame=True):
        self.use_pygame = use_pygame

        self.dimX = 1200
        self.dimY = 1000
        self.velocityD = 1
        self.taille_cube = 60
        self.taille_obstacle = 60

        self.posA = self.dimY - 300
        self.gravity = 1
        self.jump_force = -20
        self.vitesse = 5
        self.nb_obstacles = 4

        if self.use_pygame:
            import pygame
            pygame.init()

            self.screen = pygame.display.set_mode((self.dimX, self.dimY))
            pygame.display.set_caption("Runner IA")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("Arial", 40)

            self.background = pygame.image.load("background.png").convert()
            self.background = pygame.transform.scale(self.background, (self.dimX, self.dimY))

            self.ground = pygame.image.load("sol.png").convert_alpha()

            self.player_img = pygame.image.load("perso.png").convert_alpha()
            self.player_img = pygame.transform.scale(self.player_img, (self.taille_cube, self.taille_cube))
            self.player_mask = pygame.mask.from_surface(self.player_img)

            self.obstacle_img = pygame.image.load("obj.png").convert_alpha()
            self.obstacle_img = pygame.transform.scale(self.obstacle_img, (self.taille_obstacle, self.taille_obstacle))
            self.obstacle_mask = pygame.mask.from_surface(self.obstacle_img)

        self.reset()

    def reset(self):

        self.posX = 50
        self.posY = self.posA - self.taille_cube
        self.velocityY = 0
        self.score = 0
        self.running = True
        self.score = 0
        self.velocityD = 1

        self.obstacles = []
        for i in range(self.nb_obstacles):
            x = random.randint(self.dimX + i * 300, self.dimX+300 + i * 600)
            y = random.choice([
                self.posA - self.taille_cube,
                self.posA - self.taille_cube * 2
            ])
            self.obstacles.append([x, y])

    def get_state(self):
        obs = [o for o in self.obstacles if o[0] >= self.posX]
        obs.sort(key=lambda o: o[0] - self.posX)

        next_ob = obs[0]
        next2 = obs[1] if len(obs) > 1 else None

        dx = next_ob[0] - self.posX
        dy = next_ob[1]

        if next2:
            dx2 = next2[0] - self.posX
            dy2 = next2[1]
        else:
            dx2 = dy2 = 9999

        obstacle_haut = 1 if next_ob[1] != self.posA - self.taille_cube else 0

        meme_pos = None
        if next2 != None:
            meme_pos = 1 if next2[0] >= next_ob[0] + self.taille_cube else 0
        else:
            meme_pos = 0

        return (dx, dy, dx2, dy2, self.posY, obstacle_haut , meme_pos)

    def update(self, action):

        # if self.score % 500 == 0:
            #self.velocityD *= 1.2
        if action == 1 and self.posY == self.posA - self.taille_cube:
            self.velocityY = self.jump_force

        self.velocityY += self.gravity
        self.posY += self.velocityY

        if self.posY >= self.posA - self.taille_cube:
            self.posY = self.posA - self.taille_cube
            self.velocityY = 0

        for obs in self.obstacles:
            obs[0] -= self.vitesse * self.velocityD
            if obs[0] < -self.taille_obstacle:
                max_x = max ([o[0] for o in self.obstacles] )
                obs[0] = max_x + self.dimX/2
                obs[1] = random.choice([
                    self.posA - self.taille_cube,
                    self.posA - self.taille_cube * 2
                ])

        # Collision sans Pygame
        if not self.use_pygame:
            for ox, oy in self.obstacles:
                if (self.posX < ox + self.taille_obstacle and
                        self.posX + self.taille_cube > ox and
                        self.posY < oy + self.taille_obstacle and
                        self.posY + self.taille_cube > oy):
                    self.running = False
        else:
            import pygame
            player_rect = pygame.Rect(self.posX, self.posY, self.taille_cube, self.taille_cube)
            for ox, oy in self.obstacles:
                obs_rect = pygame.Rect(ox, oy, self.taille_obstacle, self.taille_obstacle)
                offset = (obs_rect.x - player_rect.x, obs_rect.y - player_rect.y)

                if self.player_mask.overlap(self.obstacle_mask, offset):
                    self.running = False

        self.score += 1

    def draw(self):
        import pygame
        if not self.use_pygame:
            return

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ground, (0, self.posA))
        self.screen.blit(self.player_img, (self.posX, self.posY))

        start_pos = (self.posX + self.taille_cube , self.posY + self.taille_cube // 2)
        end_pos = (self.posX + self.taille_cube + 5, self.posY + self.taille_cube // 2)
        pygame.draw.line(self.screen, (255, 0, 0), start_pos, end_pos, 3)





        for ox, oy in self.obstacles:
            self.screen.blit(self.obstacle_img, (ox, oy))

        score_text = self.font.render(f"Score : {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        import pygame
        pygame.display.update()



