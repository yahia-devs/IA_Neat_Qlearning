import pygame
import random

class Game:
    def __init__(self):
        pygame.init()

        self.dimX = 1200
        self.dimY = 1000
        self.taille_cube = 60
        self.taille_obstacle = 60

        self.screen = pygame.display.set_mode((self.dimX, self.dimY))
        pygame.display.set_caption("Mon jeu Pygame / IA")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 40, bold=True)

        self.background = pygame.image.load("../Images/background.png").convert()
        self.background = pygame.transform.scale(self.background, (self.dimX, self.dimY))

        self.ground = pygame.image.load("../Images/sol.png").convert_alpha()
        self.posA = self.dimY - 300  

        self.player_img = pygame.image.load("../Images/perso.png").convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (self.taille_cube, self.taille_cube))
        self.player_mask = pygame.mask.from_surface(self.player_img)

        self.obstacle_img = pygame.image.load("../Images/obj.png").convert_alpha()
        self.obstacle_img = pygame.transform.scale(self.obstacle_img, (self.taille_obstacle, self.taille_obstacle))
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_img)

        self.gravity = 1
        self.jump_force = -20
        self.vitesse = 5
        self.nb_obstacles = 4

        self.reset()

    def reset(self):
        self.posX = 50
        self.posY = self.posA - self.taille_cube
        self.velocityY = 0
        self.score = 0
        self.running = True

        self.obstacles = []
        for i in range(self.nb_obstacles):
            x = random.randint(self.dimX + i*2 * 300, self.dimX + i * 600)
            y = random.choice([
                self.posA - self.taille_cube,          
                self.posA - self.taille_cube * 2       
            ])
            self.obstacles.append([x, y])

    def get_state(self):
        obstacle_devant = [o for o in self.obstacles if o[0] >= self.posX]

        obstacle_devant.sort(key=lambda o: o[0] - self.posX)

        next_obstacle = obstacle_devant[0]
        next_next_obstacle = obstacle_devant[1] if len(obstacle_devant) > 1 else None


        dx = next_obstacle[0] - self.posX
        dy = next_obstacle[1] 

 


        if next_next_obstacle:
            dx2 = next_next_obstacle[0] - self.posX
            dy2 = next_next_obstacle[1] 
        else:
            dx2 = 9999
            dy2 = 9999

        obstacle_haut = 1 if next_obstacle[1] != self.posA - self.taille_cube   else 0 

      
        # Normalisation de la velocity (jump vs gravity)
        vel_norm = self.velocityY  # car jump_force = -20 et gravity ≈ +1

        return (dx, dy, dx2, dy2, self.posY , obstacle_haut)





    def update(self, action):

        if action == 1 and self.posY == self.posA - self.taille_cube:
            self.velocityY = self.jump_force

        self.velocityY += self.gravity
        self.posY += self.velocityY

        if self.posY >= self.posA - self.taille_cube:
            self.posY = self.posA - self.taille_cube
            self.velocityY = 0

        for obstacle in self.obstacles:
            obstacle[0] -= self.vitesse

            if obstacle[0] < -self.taille_obstacle:
                obstacle[0] = random.randint(self.dimX, self.dimX + 600)
                obstacle[1] = random.choice([
                    self.posA - self.taille_cube,
                    self.posA - self.taille_cube * 2
                ])

        player_rect = pygame.Rect(self.posX, self.posY, self.taille_cube, self.taille_cube)

        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], self.taille_obstacle, self.taille_obstacle)
            offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)

            if self.player_mask.overlap(self.obstacle_mask, offset):
                self.running = False

        self.score += 1

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ground, (0, self.posA))
        self.screen.blit(self.player_img, (self.posX, self.posY))
 
        for obstacle in self.obstacles:
            self.screen.blit(self.obstacle_img, (obstacle[0], obstacle[1]))

        score_text = self.font.render(f"Score : {int(self.score)}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

        pygame.display.update()
       # self.clock.tick(60)

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if self.running:
                keys = pygame.key.get_pressed()
                action = 1 if keys[pygame.K_SPACE] else 0
                self.update(action)
                self.draw()
            else:
                text = self.font.render("GAME OVER - SPACE pour rejouer", True, (255, 0, 0))
                self.screen.blit(text, (self.dimX//2 - 300, self.dimY//2))
                pygame.display.update()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.reset()

            self.clock.tick(60)


#if __name__ == "__main__":
 #   game = Game()
  #  while game.running:
  #      game.update(0)   # action = 0 = pas de saut (mode joueur désactivé)
   #     game.draw()

if __name__ == "__main__":
    game = Game()
    game.loop()

