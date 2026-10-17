import pygame, sys
from Plateforme import plateform

# Définition des fonctions du jeu (NE PLUS TOUCHER, sauf si nécessaire, ELLES SONT DÉJÀ COMPLÈTES)
tableau_niveau= [{"x":[200,600,400,800,425],"y":[400,200,300,400,75],"l":[150,150,150,150,150],"h":[20,20,20,20,20],"c":["bleu","bleu","rouge","rouge","jaune"],"amovible":[False,False,False,False,False]}]
# Création des plateformes (x, y, largeur, hauteur)
def get_niveau(num_niv: int)-> list:
    tab= []
    for i in range(len(tableau_niveau[num_niv]["x"])):
        tab.append(plateform(tableau_niveau[num_niv]["x"][i],tableau_niveau[num_niv]["y"][i],tableau_niveau[num_niv]["l"][i],tableau_niveau[num_niv]["h"][i],tableau_niveau[num_niv]["c"][i],tableau_niveau[num_niv]["amovible"][i]))
    return tab

def collisions_verticales(gravite):
    for obstacle in obstacles_solides:
        if player_rect.colliderect(obstacle):
            # Si le joueur tombe (mouvement vers le bas)
            if gravite > 0: 
                player_rect.bottom = obstacle.top
                gravite = 0 # Stoppe la chute pour le faire rester sur la plateforme
                
            # Si le joueur saute et tape sa tête (mouvement vers le haut)
            elif gravite < 0: 
                player_rect.top = obstacle.bottom
                gravite = 0 # Stoppe l'ascension pour le faire retomber
    return gravite #Il est nécessaire de retourner gravité car elle est modifiée dans la fonction. (C'est pas une procédure avec une valeur in out, merci ADA)

def collisions_horizontales(vitesse_x):
    for obstacle in obstacles_solides:
        if player_rect.colliderect(obstacle):
            # Si on va vers la droite, on tape le mur par la gauche de l'obstacle
            if vitesse_x > 0:
                player_rect.right = obstacle.left
            
            # Si on va vers la gauche, on tape le mur par la droite de l'obstacle
            elif vitesse_x < 0:
                player_rect.left = obstacle.right # Il n'est pas nécessaire de retourner vitesse_x, car on ne la modifie pas.

def victory():
    font = pygame.font.Font(None, 74)
    text = font.render("Gagné !", True, (255, 255, 255))
    text_rect = text.get_rect(center=(512, 288))
    fond = pygame.Surface((1024, 576))
    fond.set_alpha(128)  # Transparence
    screen.blit(fond, (0, 0))
    screen.blit(text, text_rect)

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
bouton_Y = 3

# Définition des variables du jeu

saut=0
direct= 0
screen = pygame.display.set_mode((1024, 576))
clock = pygame.time.Clock()
dt = 0
image = pygame.transform.scale(pygame.image.load("img/immobile.png").convert_alpha(), (80, 80))
tab_pos = {"0" : "img/immobile.png", "1": "img/droite.png", "2": "img/gauche.png", "10": "img/immobile.png", "11": "img/saut_d.png", "12": "img/saut_g.png"}

# TOUT CE QUI EST ICI DEVRA DISPARAITRE DANS LA VERSION FINALE, C'EST JUSTE POUR TESTER LE JEU

# Le rectangle du sol
floor_rect = pygame.Rect(0, 526, 1024, 50)

niveau_actuelle = get_niveau(0)
couleur_plat_actu ={"rouge" :[],"bleu": [], "jaune": []}
for i in niveau_actuelle :
    i.cree_plat()
    couleur_plat_actu[i.get_couleur()].append(i.get_plat())
# Jusqu'ici. À moins de s'en servir pour créer l'écran de start (éléments de déco, pourquoi pas...)

# État du jeu : True = Bleu solide, False = Rouge solide
bleu_actif = True 

player_rect = image.get_rect(topleft=(50, 400))
gravite = 0
vitesse_x = 0

while True:
    # 1. DÉFINITION DES OBSTACLES ACTIFS
    # On crée une liste contenant le sol + la couleur actuellement active
    obstacles_solides = [floor_rect, couleur_plat_actu["jaune"][0]]
    if bleu_actif:
        obstacles_solides.extend(couleur_plat_actu["bleu"])
    else:
        obstacles_solides.extend(couleur_plat_actu["rouge"])

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

    # On vérifie les collisions verticales

    gravite = collisions_verticales(gravite) #Ici, on est obligé de récupérer la valeur de gravité, car sinon le joueur accumulerait la gravité et tomberait à travers les plateformes.

    # On vérifie les collisions horizontales
    
    player_rect.x += vitesse_x

    collisions_horizontales(vitesse_x) #Par contre ici, on ne récupère pas la valeur de vitesse_x, car on ne la modifie pas dans la fonction.

    if controller is None : 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            direct=2
            vitesse_x = -300 * dt
        elif keys[pygame.K_d]:
            direct=1
            vitesse_x = 300 * dt
        else:
            direct=0
            vitesse_x = 0
    else :
        hat_x, hat_y = controller.get_hat(0)
        if hat_x == -1:  # Croix vers la gauche
            vitesse_x = -300 * dt
            direct=2
        elif hat_x == 1:  # Croix vers la droite
            vitesse_x = 300 * dt
            direct=1
        else:
            direct=0
            vitesse_x = 0
    
    # --- AFFICHAGE ---

    screen.fill((50, 50, 50))
    
    # On dessine le sol (gris clair)

    pygame.draw.rect(screen, (100, 100, 100), floor_rect)
    
    
    for i in niveau_actuelle:
        i.affiche_plat(bleu_actif,screen)
    # On dessine le joueur

    image = pygame.transform.scale(pygame.image.load(tab_pos[str(direct+saut)]).convert_alpha(), (80, 80))
    screen.blit(image, player_rect)

    # Dessinn de la plateforme jaune (toujours pleine)

    # Logique de victoire

    if player_rect.bottom == couleur_plat_actu["jaune"][0].top:
        victory()
    
    pygame.display.update()
    dt = clock.tick(60) / 1000