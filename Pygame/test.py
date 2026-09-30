import pygame, sys, random

def draw_floor(): #création des deux sols pour créer la transition quand le premier sol disparait
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos + 576/2,450))

def create_pipe():
    random_pipe_pos = random.randint(200,400)
    # random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_pipe_pos-150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512 :
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,bird_movement*-5,1)
    return new_bird 


pygame.init() # Lancement de Pygame
screen = pygame.display.set_mode((576/2,1024/2)) # Création de l'écran du jeu (format d'écran)
clock = pygame.time.Clock() # Horloge interne du jeu

# Game Variables
gravity = 0.125
bird_movement = -2
game_active = True

bg_surface = pygame.image.load('sprites/background-day.png').convert() # import du background du jeu (on en crée une surface)

floor_surface = pygame.image.load("sprites/base.png").convert() #Import du sol du jeu
floor_x_pos = 0 # cord horizontal du sol (utile pour le déplacer après)

bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
bird_rect = bird_surface.get_rect(center = (50,256))

pipe_surface = pygame.image.load('sprites/pipe-green.png')
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
# pipe_height = [200,250,300,350,400]

while True: # Boucle qui fait tourner le jeu
    for event in pygame.event.get(): # Boucle qui chope tous les events (souris, clavier, etc)
        if event.type == pygame.QUIT: # Quitter le jeu
            pygame.quit() 
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -4.5
            if event.key == pygame.K_SPACE and not(game_active):
                game_active = True
                pipe_list = []
                bird_rect.center = (50,256)
                bird_movement = -1.5
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())


    # Rajout des images etc
    screen.blit(bg_surface,(0,0)) # On superpose l'écran demandé à l'écran actuel ((0,0) car c'est le coin haut gauche de l'écran))

    # S'active quand le jeu est en cours.
    if game_active:
        # Bird
        bird_movement = bird_movement + gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement 
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collisions(pipe_list)
        # Pipes

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos = floor_x_pos - 2 # Déplace le sol
    draw_floor() # rajoute le sol
    if floor_x_pos <= -288:
        floor_x_pos = 0 # crée cette transition quand le premier sol disparait.
    

    pygame.display.update() # Update de l'écran du jeu
    clock.tick(120) # Limite les fps à 120




