import pygame

class plateform :
    def __init__(self, x: int,y: int, largeur: int,hauteur: int, couleur: str, movible: bool):
        self.x = x
        self.y = y
        self.h = hauteur
        self.l = largeur
        self.c = couleur
        self.m = movible
    def cree_plat (self):
        self.plat = pygame.Rect(self.x, self.y, self.l, self.h)

    def affiche_plat(self,bleu_act : bool,ecran):
        if self.c == "bleu" :
            if bleu_act:
                pygame.draw.rect(ecran, (100, 150, 255), self.plat) # Pleine
            else:
                pygame.draw.rect(ecran, (100, 150, 255), self.plat, 2)
        elif self.c == "rouge": 
            if not bleu_act:
                pygame.draw.rect(ecran, (255, 100, 100), self.plat) # Pleine
            else:
                pygame.draw.rect(ecran, (255, 100, 100), self.plat, 2) # Vide (juste le contour)
        else:
            pygame.draw.rect(ecran, (255, 255, 100), self.plat)
