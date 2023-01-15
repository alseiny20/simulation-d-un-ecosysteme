import time
from random import *
import pygame


class Espece:
    def __init__(self, nom="espece"):
        self.x = None
        self.y = None
        self.nom = nom
        self.logo = self.nom[0].upper()

    def __repr__(self):
        return self.logo


class Ressource(Espece):

    def __init__(self, nourrissant=1, nom="resource"):
        Espece.__init__(self, nom)
        self.nourrissant = nourrissant


class Logo(pygame.sprite.Sprite):

    def __init__(self, x, y, acc):
        """
        La ligne ci-dessous est importante car elle permet d'appeler le
        constructeur de la classe 'pygame.sprite.Sprite', ce qui est
        obligatoire dans un processus d'héritage.
        """
        pygame.sprite.Sprite.__init__(self)

        """
        Un Sprite doit posséder au moins deux attributs 'self.image' et
        'self.rect'. Les noms ne doivent pas changer. 'self.image' doit
        contenir une Surface correspondant au dessin du Sprite (ici une
        image chargée). 'self.rect' est le rectangle où il faudra 
        dessiner l'image. Ici, nous initialisons 'self.rect' à la taille
        de 'self.image' puis nous le déplaçons selon les paramètres du
        constructeur de Ball. 
        """
        if hasattr(self, 'genre'):
            self.image = pygame.image.load("Image/" + self.nom + self.genre + ".png")

        else:
            self.image = pygame.image.load("Image/" + self.nom + str(1) + ".png")

        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.v =acc

    def update(self):
        """Cette méthode est appelée régulièrement pour modifier le rectangle d'
        affichage de la l'espece en fonction de ses cordonné (x, y)
        et de sa vitesse."""
        self.rect.centerx, self.rect.centery = self.x+15, self.y+15
        

class Vivant(Espece):

    def __init__(self, vie,rayon, reproduit, parent, nom="vivant"):
        Espece.__init__(self, nom)
        self.inlive = True
        self.enceinte = False
        self.vie_max = vie
        self.energie = vie
        self.rayon = rayon
        self.parent = parent
        self.reproduit = reproduit
        self.genre = choice(["male", "femelle"])


    def mourir(self):
        self.energie = 0
        self.inlive = False


class Etre_vivant(Vivant, Logo):

    def __init__(self, nourriture, vie,rayon, reproduit, parent, x, y, acc, nom="etreVivant"):
        Vivant.__init__(self, vie,rayon, reproduit, parent, nom)
        Logo.__init__(self, x, y, acc)
        self.nourriture = nourriture
        self.nom = nom

    def mange(self, e):
        if self.inlive and e.nom in self.nourriture:
##            print(self.nom, "mange", e.nom)
            self.energie = min(self.energie + e.nourrissant, self.vie_max)


class Carnivore(Etre_vivant):

    def __init__(self, nourriture, vie, rayon, reproduit, parent, x, y, acc, nom="predateur"):
        Etre_vivant.__init__(self, nourriture, vie, rayon, reproduit, parent, x, y, acc, nom)

    def mange(self, e):
        Etre_vivant.mange(self, e)
        e.mourir()


class Lion(Carnivore):

    def __init__(self):
        Carnivore.__init__(self, ("gazelle",), 60, 300, True, None, 0, 0, 2, "lion")


    def reproduction(self, terrain, mere, pere):
        new = Lion()
        new.parent = mere
        mere.enceinte = True
        pere.reproduit = False
        terrain.nouveau_nee.append(new)
##        print("reproduction", new.nom)


class Gazelle(Etre_vivant, Ressource, Logo):

    def __init__(self):
        Etre_vivant.__init__(self, ('herbe',), 150, 150, True, None, 0, 0, 1, "gazelle")
        Ressource.__init__(self, 5, "gazelle")

    def reproduction(self, terrain, mere, pere):
        new = Gazelle()
        new.parent = mere
        mere.enceinte = True
        pere.reproduit = False
        terrain.nouveau_nee.append(new)
##        print("reproduction", new.nom)


class Herbe(Ressource, Logo):

    def __init__(self):
        Ressource.__init__(self, 1, "herbe")
        Logo.__init__(self, 0, 0, 0)
        self.nourriture = []

