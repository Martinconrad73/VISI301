import pygame, sys

# Définition des fonctions du jeu

# Initialisation de Pygame et création de la fenêtre

pygame.init()
pygame.joystick.init() #initialisation de la manette
controller = None
if pygame.joystick.get_count() > 0:
    controller = pygame.joystick.Joystick(0)
    controller.init()
bouton_X = 2
bouton_A = 0
bouton_B = 1
bouton_y = 3

# Définition des variables du jeu

saut=0
direct= 0
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()
dt = 0
image = pygame.transform.scale(pygame.image.load("img/immobile.png").convert_alpha(), (80, 80))

# Le rectangle du sol
floor_rect = pygame.Rect(0, 526, 1024, 50)
tab_pos = {"0" : "img/immobile.png", "1": "img/droite.png", "2": "img/gauche.png", "10": "img/immobile.png", "11": "img/saut_d.png", "12": "img/saut_g.png"}

# Création des plateformes (x, y, largeur, hauteur)
plateformes_bleues = [pygame.Rect(200, 400, 150, 20), pygame.Rect(600, 200, 150, 20)]
plateformes_rouges = [pygame.Rect(400, 300, 150, 20), pygame.Rect(800, 400, 150, 20)]
plateforme_jaune = pygame.Rect(500, 100, 150, 20)

# État du jeu : True = Bleu solide, False = Rouge solide
bleu_actif = True 

player_rect = image.get_rect(topleft=(50, 400))
gravite = 0

while True:
    # 1. DÉFINITION DES OBSTACLES ACTIFS
    # On crée une liste contenant le sol + la couleur actuellement active
    obstacles_solides = [floor_rect, plateforme_jaune]
    if bleu_actif:
        obstacles_solides.extend(plateformes_bleues)
    else:
        obstacles_solides.extend(plateformes_rouges)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        if controller is None :  # Touches Ordinateur
            if event.type == pygame.KEYDOWN: 
                # --- SAUT ---
                if event.key == pygame.K_SPACE:
                    saut=10
                    
                    # On vérifie si on touche un des obstacles solides
                    for obstacle in obstacles_solides:
                        # Si le joueur est aligné en Y et au-dessus en X
                        if player_rect.bottom == obstacle.top and player_rect.right > obstacle.left and player_rect.left < obstacle.right:
                            gravite = -12
                            saut= 0
                            bleu_actif = not bleu_actif # Inverse l'état (True devient False, et inversement)
                            break # On arrête de chercher, on a trouvé le sol
                    
        else : #Touches Manette générique
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == bouton_A:
                    saut=10
                    # On vérifie si on touche un des obstacles solides
                    for obstacle in obstacles_solides:
                    # Si le joueur est aligné en Y et au-dessus en X
                        if player_rect.bottom == obstacle.top and player_rect.right > obstacle.left and player_rect.left < obstacle.right:
                            gravite = -12
                            bleu_actif = not bleu_actif # Inverse l'état (True devient False, et inversement)
                            saut = 0
                            break # On arrête de chercher, on a trouvé le sol
                    
    # --- LOGIQUE DE MOUVEMENT ---
    
    gravite += 0.5 
    player_rect.y += gravite

    # 2. LA DÉTECTION DE COLLISION (sur la liste des obstacles)
    for obstacle in obstacles_solides:
        if player_rect.colliderect(obstacle):
            if gravite >= 0: # Si le joueur tombe vers le bas
                player_rect.bottom = obstacle.top
                gravite = 0
    if controller is None : 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_q]:
            direct=2
            player_rect.x -= 300 * dt
        elif keys[pygame.K_d]:
            direct=1
            player_rect.x += 300 * dt
        else:
            direct=0
    else :
        hat_x, hat_y = controller.get_hat(0)
        if hat_x == -1:  # Croix vers la gauche
            player_rect.x -= 300 * dt
            direct=2
        elif hat_x == 1:  # Croix vers la droite
            player_rect.x += 300 * dt
            direct=1
        else:
            direct=0
    
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
    image = pygame.transform.scale(pygame.image.load(tab_pos[str(direct+saut)]).convert_alpha(), (80, 80))
    screen.blit(image, player_rect)
    # Dessinn de la plateforme jaune (toujours pleine)
    
    pygame.draw.rect(screen, (255, 255, 100), plateforme_jaune)

    # Logique de victoire

    if player_rect.bottom == plateforme_jaune.top:
        font = pygame.font.Font(None, 74)
        text = font.render("Gagné !", True, (255, 255, 255))
        text_rect = text.get_rect(center=(512, 288))
        screen.blit(text, text_rect)
    
    pygame.display.update()
    dt = clock.tick(60) / 1000