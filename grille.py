import math
import os
import sys
import time
from random import randint
from espece import *

'''import pygame
import matplotlib as plt'''
import random

class Tab:

    def __init__(self, largeur, hauteur):
        self.hauteur = hauteur
        self.largeur = largeur
        self.zon = []
        for i in range(largeur):
            self.zon.append(["."] * hauteur)

    def resetTab(self):
        """" fonction de reinitialisation de la grille"""
        for i in range(self.largeur):
            for j in range(self.hauteur):
                self.zon[i][j] = "."

    def affichtab(self):
        """fonction d'affichage de la grille"""
        for i in range(len(self.zon)):
            for j in range(len(self.zon[i])):
                print(self.zon[i][j], end=" ")
            print("\n")


class Terrain(Tab):

    def __init__(self, x, y):
        Tab.__init__(self, x, y)
        self.temps = 0
        self.nbr_jour = 0
        self.jour = False
        self.composant = pygame.sprite.Group()
        self.nouveau_nee = []
        self.liste_lion = []
        self.liste_gazelle = []
        self.liste_herbe = []
        self.liste_jour = []
        self.legende = True

        pygame.init()
        pygame.display.set_caption("Mon jeux")
        self.ecran = None

    def creation(self, espece):
        self.composant.add(espece)

    def move_element(self):
        """Supression d'un element parmi les composants du terrain lorsqu'ils ne sont plus en vie"""
        for element in self.composant:
            if hasattr(element, 'inlive') and not element.inlive:
                print(element, "est MORT")
                self.composant.remove(element)

    def croisement(self):
        """"la fonction croisement se chargera de cibler l'action qui a eu lieu lors du croisment entre des composants de
        l'ecosysteme : soit se nourrir, soit se reproduire """
        for element in self.composant:
            for element2 in self.composant:
                if pygame.sprite.collide_rect(element, element2):
                    if element2.nom in element.nourriture:
                        element.mange(element2)
                    elif element.nom == element2.nom and element != element2 and hasattr(element, 'inlive') and hasattr(
                            element2, 'inlive'):
                        if (element.genre == "male" and element.reproduit == True) and (
                                element2.genre == "femelle" and element2.enceinte == False):
                            element.reproduction(self, element2, element)
                        elif (element.genre == "femelle" and element.enceinte == False) and (
                                element2.genre == "male" and element2.reproduit == True):
                            element.reproduction(self, element, element2)

    def equilibrage(self):
        for element in self.composant:
            self.zon[element.x][element.y] = element.logo
            if hasattr(element, "inlive"):
                if element.genre == "male":
                    element.reproduit = True
                if not (element.parent in self.composant):
                    element.parent = None

    def mise_a_jour(self):

        self.croisement()
        self.move_element()
        #self.resetTab()
        self.equilibrage()
        #self.affichtab()
        #time.sleep(2)
        #os.system('clear')


    def moment(self):
        """fonction de gestion du temps qui renvoie une couleur rgb suivant l'évolution de l'écosysteme"""
        if self.jour:
            self.temps -= 0.5
            if self.temps < 2:
                self.jour = False
        else:
            self.temps += 0.5
            if self.temps > 253:
                self.jour = True
        pygame.mixer.music.set_volume(abs(self.temps + 100) / 1000)
        return pygame.Color(int(self.temps), int(self.temps), int(self.temps))

    def alea_posi(self, espece):
        """Fonction d'affectation aléatoire de coordonnées """
        if espece.x is None:
            espece.rect.x = espece.x = randint(0, self.largeur - 1)
            espece.rect.y = espece.y = randint(0, self.hauteur - 1)

    def gestion_energie(self):
        """fonction de traitement de l'energie pour l'ensemble des etres vivants de l'écosysteme"""
        for element in self.composant:
            if hasattr(element, "inlive"):
                element.energie -= 20
                if element.energie < 0:
                    element.inlive = False

    def test_vivants(self):
        """fonction de verification du nombre d'etre vivant restant dans l'écosysteme"""
        a = len([p for p in self.composant if hasattr(p, "inlive")])
        if a > 0:
            return True
        else:
            return False

    def enregistrement_naissance(self):
        """fonction de mise a terme de la reproduction elle finalise la reproduction d'une espece et le remet en
        etat de se reproduire"""
        for nouveau in self.nouveau_nee:
            self.alea_posi(nouveau)
            if nouveau.parent in self.composant:
                self.composant.add(nouveau)
        self.nouveau_nee = []

        for element in self.composant:
            if hasattr(element, 'inlive'):
                element.reproduit = True
                element.enceinte = False

    def deplacement_alea(self, espece):
        """fonction de deplacement aleatoire d'une espece"""
        d = 1
        if self.largeur - 2 > espece.x > 1:
            if randint(0, 1):
                espece.x += d
            else:
                espece.x -= d
        elif espece.x < self.largeur - 1:
            espece.x += d
        else:
            espece.x -= d
        if self.hauteur - 10 > espece.y > 1:
            if randint(0, 1):
                espece.y += d
            else:
                espece.y -= d
        elif espece.y < self.hauteur - 1:
            espece.y += d
        else:
            espece.y -= d

    def deplacement(self, espece):
        """fonction de deplacement  avec intelligence artificielle qui vérifira, pour un predateur, la cible la plus proche
        dans son rayon de vision. Cette fonction  orientera le prédateur vers la cible la plus procge, seulement lorsque le prédateur
        sera en dessous d'un seuil d'énergie fixé. Par cette fonction, la proie repèrera le danger le plus proche (donc un prédateur)
        et s'en éloignera le plus possible."""
        cible_potentiel = []
        cible = None
        have_cible = False
        if espece.nom == 'lion' and espece.energie < espece.vie_max * 0.5:
            for i in self.composant:
                distance = math.sqrt((espece.x - i.x) ** 2 + (espece.y - i.y) ** 2)
                if i.nom in espece.nourriture and distance < espece.rayon:
                    have_cible = True
                    cible_potentiel.append(distance)

                    if min(cible_potentiel) == distance:
                        cible = i
            if have_cible:
                ##                print('jai une simble a', distance)
                if cible.x < espece.x and cible.y < espece.y:

                    if randint(0, 1):
                        espece.x -= 1
                    else:
                        espece.y -= 1
                else:
                    if cible.x > espece.x:
                        espece.x += 1
                    else:
                        espece.x -= 1
                    if cible.y > espece.y:
                        espece.y += 1
                    else:
                        espece.y -= 1
            if not have_cible:
                self.deplacement_alea(espece)
        predateur_potentiel = []
        predateur = None
        have_predateur = False
        if espece.nom == 'gazelle':
            for i in self.composant:
                distance = math.sqrt((espece.x - i.x) ** 2 + (espece.y - i.y) ** 2)
                if espece.nom in i.nourriture and distance < espece.rayon:
                    have_predateur = True
                    predateur_potentiel.append(distance)

                    if min(predateur_potentiel) == distance:
                        predateur = i
            if have_predateur:
                ##                print('jai un predateur a', distance)
                if predateur.x < espece.x and predateur.y < espece.y:
                    if espece.x < self.largeur - 1 and espece.y < self.hauteur - 1:
                        if randint(0, 1):
                            espece.x += 1
                        else:
                            espece.y += 1
                else:
                    if predateur.x > espece.x > 1:
                        espece.x -= 1
                    elif espece.x < self.largeur - 1:
                        espece.x += 1
                    if predateur.y > espece.y > 1:
                        espece.y -= 1
                    elif espece.y < self.hauteur - 1:
                        espece.y += 1
            if not have_predateur:
                self.deplacement_alea(espece)
        else:
            self.deplacement_alea(espece)

    def graphique(self):
        self.liste_jour.append(self.nbr_jour)

        self.nbr_lion = 0
        self.nbr_gazelle = 0
        self.nbr_herbe = 0

        for animal in self.composant:
            if animal.nom == 'lion':
                self.nbr_lion += 1
            elif animal.nom == 'gazelle':
                self.nbr_gazelle += 1
            else:
                self.nbr_herbe += 1
        self.liste_lion.append(self.nbr_lion)
        self.liste_gazelle.append(self.nbr_gazelle)
        self.liste_herbe.append(self.nbr_herbe)

        plt.ion()

        plt.plot(self.liste_jour, self.liste_lion, label='Lion', color='red', marker='x')
        plt.plot(self.liste_jour, self.liste_gazelle, label='Gazelle', color='gold', marker='x')
        plt.plot(self.liste_jour, self.liste_herbe, label='Herbe', color='green', marker='x')
        if self.legende:
            plt.legend()
            plt.grid()
            self.legende = False

        plt.title('Evolution des espèces en fonction du temps')
        plt.xlabel('Jours')
        plt.ylabel("Nombres d'animaux")

        plt.show()

        plt.pause(0.001)

    def evolution(self):

        """Fonction d'évolution de l'écosysteme pour un jour
        dans cette fonction nous affecteron aléatoirement des coordonées au divers espèces initialement
        introduitent dans le terrain, nous ferons un appel de l'ensemble des fonction du programme qui gère son
        evolution, les déplacememnt des espèce ainsi que leur representation sur la grille et la mise a jour de leur
        coordonées sur l'interface. la fonction #mise_ajour c'est chargera de verifier les colisions ainsi que
        les action necessaire (manger, se reprodure, .....) qui tournera dans la boucle (500) et représentera la moitié d'une journée"""

        """"A la fin de chaque journée sera appelé les fonction de gestion d'energie ainsi que le traitement 
        des naissances"""

        self.ecran = pygame.display.set_mode((self.largeur + 30, self.hauteur + 35))
        #self.graphique()

        for i in range(500):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (pygame.mouse.get_pressed()[0]):
                        a = Gazelle()
                        self.composant.add(a)
                        a.rect.x, a.rect.y = a.x, a.y = event.pos[0], event.pos[1]
                    elif (pygame.mouse.get_pressed()[2]):
                        a = Lion()
                        a.rect.x, a.rect.y = a.x, a.y = event.pos[0], event.pos[1]
                        self.composant.add(a)
                    elif (pygame.mouse.get_pressed()[1]):
                        s = Gazelle()
                        s.rect.x, s.rect.y = s.x, s.y = event.pos[0], event.pos[1]
                        for element in self.composant:
                            if pygame.sprite.collide_rect(element, s):
                                element.kill()
                                s.kill()

            self.ecran.fill(self.moment())
            for espece in self.composant:
                if hasattr(espece, 'inlive'):
                    self.deplacement(espece)
            '''for espece in self.composant:
                if espece.nom == 'herbe':
                    espece.image = pygame.image.load("Image/" + espece.nom + str(1)+'_'+str(random.randint(1,4))+".png")
                    espece.image = pygame.transform.scale(espece.image, (40, 40))
                    espece.rect = espece.image.get_rect()'''
            self.composant.update()
            self.mise_a_jour()
            self.composant.draw(self.ecran)
            pygame.display.flip()
            pygame.time.delay(10)
        self.gestion_energie()
        self.enregistrement_naissance()
        self.nbr_jour += 0.5
