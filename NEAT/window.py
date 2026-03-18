import pygame
import random

pygame.init()

dimX = 1200
dimY = 1000
taille_cube = 60
taille_obstacle = 60

screen = pygame.display.set_mode((dimX, dimY))
pygame.display.set_caption("Mon jeu Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40, bold=True)

background = pygame.image.load("../Images/background.png").convert()
background = pygame.transform.scale(background, (dimX, dimY))

ground = pygame.image.load("../Images/sol.png").convert_alpha()

ground_height = dimY - 300                
posA = ground_height                     

player_img = pygame.image.load("../Images/perso.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (taille_cube, taille_cube))
player_mask = pygame.mask.from_surface(player_img)   

obstacle_img = pygame.image.load("../Images/obj.png").convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (taille_obstacle, taille_obstacle))
obstacle_mask = pygame.mask.from_surface(obstacle_img)

posX = 50
posY = posA - taille_cube-20

gravity = 1
velocityY = 0
jump_force = -20
vitesse = 7                                 


def reset_game():
    global posY, velocityY, obstacles, score, running

    posY = posA - taille_cube
    velocityY = 0
    score = 0
    running = True

    obstacles = []
    for i in range(nb_obstacles):
        x = random.randint(dimX + i * 300, dimX + i * 600)
        y = random.choice([posA - taille_cube, posA - taille_cube * 2])
        obstacles.append([x, y])


nb_obstacles = 4
reset_game()


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    touches = pygame.key.get_pressed()

    if not running:
        text1 = font.render(" GAME OVER ", True, (255, 0, 0))
        text2 = font.render("Appuie ESPACE pour rejouer", True, (255, 255, 255))
        text3 = font.render(f"Score : {int(score)}", True, (255, 255, 255))

        screen.blit(background, (0, 0))
        screen.blit(text1, (dimX//2 - 200, dimY//2 - 120))
        screen.blit(text3, (dimX//2 - 70, dimY//2 - 40))
        screen.blit(text2, (dimX//2 - 300, dimY//2 + 40))
        pygame.display.update()

        if touches[pygame.K_SPACE]:
            reset_game()
        continue

    score += 1


    if touches[pygame.K_SPACE] and posY == posA - taille_cube:
        velocityY = jump_force

    velocityY += gravity
    posY += velocityY

    if posY >= posA - taille_cube:
        posY = posA - taille_cube
        velocityY = 0


    for obstacle in obstacles:
        obstacle[0] -= vitesse

        if obstacle[0] < -taille_obstacle:
            obstacle[0] = random.randint(dimX, dimX + 500)
            obstacle[1] = random.choice([posA - taille_cube, posA - taille_cube * 2])


    player_rect = pygame.Rect(posX, posY, taille_cube, taille_cube)

    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], taille_obstacle, taille_obstacle)

        offset = (obstacle_rect.x - player_rect.x, obstacle_rect.y - player_rect.y)

        if player_mask.overlap(obstacle_mask, offset):
            running = False



    screen.blit(background, (0, 0))
    screen.blit(ground, (0, posA))

    screen.blit(player_img, (posX, posY))

    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

    score_text = font.render(f"Score : {int(score)}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.update()
    clock.tick(60)
