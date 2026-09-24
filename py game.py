import pygame
import sys

pygame.init()
if pygame.joystick.get_count() == 1:
    manette = pygame.joystick.Joystick(0)
    manette.init()
    print("Manette détectée :", manette.get_name())
    controleur= True
else:
    controleur= False
perso_surface=pygame.image.load("perso.png").convert_alpha()
perso_pos = (1280/2,720/2)


while True:
    background.fill((0, 100, 0))
    screen.blit(background, (0, 0))
    screen.blit(perso_surface, perso_pos)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.JOYHATMOTION:

            # Croix vers le haut
            if event.value[1] == 1:
                perso_pos = (perso_pos[0], perso_pos[1] - 10)

            # Croix vers le bas
            if event.value[1] == -1:
                perso_pos = (perso_pos[0], perso_pos[1] + 10)

            # Croix vers la gauche
            if event.value[0] == -1:
                perso_pos = (perso_pos[0] - 10, perso_pos[1])

            # Croix vers la droite
            if event.value[0] == 1:
                perso_pos = (perso_pos[0] + 10, perso_pos[1])