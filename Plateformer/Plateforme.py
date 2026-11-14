import pygame

class plateform :
    def __init__(self, x: int,y: int, largeur: int,hauteur: int, couleur: str, m_direction: str,m_lim: int):
        self.x = x
        self.y = y
        self.h = hauteur
        self.l = largeur
        self.c = couleur
        self.m_lim= (-1*m_lim,m_lim)
        self.c_m= 0
        self.m_direction = m_direction #G = gauche, D = droite, H = haut, B = bas, N = pas de mouvement
        if self.c == "bleu":
            self.image = pygame.transform.scale(pygame.image.load("img/bleu.png").convert_alpha(), (self.l, self.h))
        elif self.c == "rouge":
            self.image = pygame.transform.scale(pygame.image.load("img/rouge.png").convert_alpha(), (self.l, self.h))
        elif self.c == "jaune":
            self.image = pygame.transform.scale(pygame.image.load("img/jaune.png").convert_alpha(), (self.l, self.h))
    def get_couleur(self):
        return self.c
    
    def cree_plat (self):
        if self.m_direction != "N":
            if self.m_direction == "G" and self.c_m == self.m_lim[0]:
                self.m_direction = "D"
            elif self.m_direction == "D" and self.c_m == self.m_lim[1]:
                self.m_direction = "G"
            elif self.m_direction == "H" and self.c_m == self.m_lim[0]:
                self.m_direction = "B"
            elif self.m_direction == "B" and self.c_m == self.m_lim[1]:
                self.m_direction = "H"
            self.mouvement_movible()
        self.plat = pygame.Rect(self.x, self.y, self.l, self.h)
    def get_plat(self):
        return self.plat
    def affiche_plat(self,bleu_act : bool,ecran):
        if self.m_direction != "N":
            self.cree_plat()
        if self.c == "bleu" :
            if bleu_act:
                ecran.blit(self.image, self.plat)
            else:
                pygame.draw.rect(ecran, (100, 150, 255), self.plat, 2)
        elif self.c == "rouge": 
            if not bleu_act:
                ecran.blit(self.image, self.plat)
            else:
                pygame.draw.rect(ecran, (255, 100, 100), self.plat, 2) # Vide (juste le contour)
        else:
            ecran.blit(self.image, self.plat)
    def mouvement_movible(self):
        if self.m_direction == "G":
            self.x -= 1
            self.c_m -=1
        elif self.m_direction == "D":
            self.x += 1
            self.c_m +=1
        elif self.m_direction == "H":
            self.y -= 1
            self.c_m -=1
        elif self.m_direction == "B":
            self.y += 1
            self.c_m +=1