import pygame, sys

pygame.init()
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()
dt = 0

# Le rectangle du sol
floor_rect = pygame.Rect(0, 526, 1024, 50)

# Création des plateformes (x, y, largeur, hauteur)
plateformes_bleues = [pygame.Rect(200, 400, 150, 20), pygame.Rect(600, 200, 150, 20)]
plateformes_rouges = [pygame.Rect(400, 300, 150, 20), pygame.Rect(800, 400, 150, 20)]

# État du jeu : True = Bleu solide, False = Rouge solide
bleu_actif = True 

player_rect = pygame.Rect(492, 100, 40, 40)
gravite = 0

while True:
    # 1. DÉFINITION DES OBSTACLES ACTIFS
    # On crée une liste contenant le sol + la couleur actuellement active
    obstacles_solides = [floor_rect]
    if bleu_actif:
        obstacles_solides.extend(plateformes_bleues)
    else:
        obstacles_solides.extend(plateformes_rouges)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
            
        if event.type == pygame.KEYDOWN: 
            # --- SAUT ---
            if event.key == pygame.K_SPACE:
                # On vérifie si on touche un des obstacles solides
                for obstacle in obstacles_solides:
                    # Si le joueur est aligné en Y et au-dessus en X
                    if player_rect.bottom == obstacle.top and player_rect.right > obstacle.left and player_rect.left < obstacle.right:
                        gravite = -12
                        break # On arrête de chercher, on a trouvé le sol
            
            # --- SWITCH BLEU/ROUGE ---
            if event.key == pygame.K_w: # Touche "Entrée" pour switcher
                bleu_actif = not bleu_actif # Inverse l'état (True devient False, et inversement)

    # --- LOGIQUE DE MOUVEMENT ---
    
    gravite += 0.5 
    player_rect.y += gravite

    # 2. LA DÉTECTION DE COLLISION (sur la liste des obstacles)
    for obstacle in obstacles_solides:
        if player_rect.colliderect(obstacle):
            if gravite >= 0: # Si le joueur tombe vers le bas
                player_rect.bottom = obstacle.top
                gravite = 0

    keys = pygame.key.get_pressed() 
    if keys[pygame.K_q]:
        player_rect.x -= 300 * dt
    if keys[pygame.K_d]:
        player_rect.x += 300 * dt
    
    # --- AFFICHAGE ---
    screen.fill((50, 50, 50))
    
    # On dessine le sol (gris clair)
    pygame.draw.rect(screen, (100, 100, 100), floor_rect)
    
    # DESSIN DES PLATEFORMES BLEUES
    for plat in plateformes_bleues:
        if bleu_actif:
            pygame.draw.rect(screen, (100, 150, 255), plat) # Pleine
        else:
            pygame.draw.rect(screen, (100, 150, 255), plat, 2) # Vide (juste le contour)

    # DESSIN DES PLATEFORMES ROUGES
    for plat in plateformes_rouges:
        if not bleu_actif:
            pygame.draw.rect(screen, (255, 100, 100), plat) # Pleine
        else:
            pygame.draw.rect(screen, (255, 100, 100), plat, 2) # Vide (juste le contour)

    # On dessine le joueur (en blanc pour contraster)
    pygame.draw.rect(screen, (255, 255, 255), player_rect)
    
    pygame.display.update()
    dt = clock.tick(60) / 1000