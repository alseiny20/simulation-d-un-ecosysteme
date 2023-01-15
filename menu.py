import math
from tkinter import *
from espece import *
from grille import Terrain

class Simulation(Tk):
    """Definition du menu avec une fenetre tekinter coportant 3 label et zone de saisie ainsi que deux bouton
    demarage et aret de la sumulation qui retourne le nombre de lion, de gazelle ainsi que la quantié dherbe
     initial de la sumulation qui sera entrer par lululisateur"""

    def __init__(self,largeur,hauteur):

        Tk.__init__(self)

        self.title("Menu Ecosystem")
        self.geometry('500x300')
        self.can = Canvas(self, width=500, height=300)
        self.filename = PhotoImage(file="Image/ecosystem.png")
        self.can.create_image(0, 0, anchor=NW, image= self.filename)
        self.can.place(x=0, y=0)

        self.play = Button(self, text='play ', command=self.initialisation, relief=RIDGE)
        self.exit = Button(self, text='Quitter la simulation', command=self.quit, relief=GROOVE)

        self.zone_lion = Label(self, text="Veuillez saisir le Nombre de Lion", fg='red', )
        self.zone_gazelle = Label(self, text="Veuillez saisir le Nombre de Gazelle", fg='blue')
        self.zone_herbe = Label(self, text="Veuillez saisir la Quantité d'herbe", fg='green')

        self.nb_lion = Entry(self)
        self.nb_lion.insert(0, "20")
        self.nb_gazelle = Entry(self)
        self.nb_gazelle.insert(0, "60")
        self.qt_herbe = Entry(self)
        self.qt_herbe.insert(0, "100")

        self.zone_lion.pack()
        self.nb_lion.pack()

        self.zone_gazelle.pack()
        self.nb_gazelle.pack()

        self.zone_herbe.pack()
        self.qt_herbe.pack()

        self.play.pack()
        self.exit.pack()

        self.terrain = Terrain(largeur, hauteur)
        self.nombre_de_lion, self.nombre_de_gazelle, self.quantite_dherbe = 0, 0, 0
        self.execution = False
        pygame.mixer.music.load("Audio/generique_savane.wav")
        pygame.mixer.music.play()


    def initialisation(self):
        """Fonction d'intialisation de la simulation appel une fenetre tkinter et recupere les valeur entrer
        puis qui cree les espece """
        pygame.mixer.music.stop()
        for i in range(int(self.qt_herbe.get())):
            self.terrain.creation(Herbe())
        for i in range(int(self.nb_lion.get())):
            self.terrain.creation(Lion())
        for i in range(int(self.nb_gazelle.get())):
            self.terrain.creation(Gazelle())
        for element in self.terrain.composant:
              self.terrain.alea_posi(element)
        self.evolution()

    def evolution(self):
        """Fonction devolution de l'ecosysteme d'un jour
        dans cette fonction nous affecton alleatoirement des coordonéé au divers espece initialement
        introduite dans le terrain puis puis l'appel de l'ensemble des fonction du programme qui gere son
        evolution deplacememnt sur des espece ainsi que leur representation sur la grille et la mise a jour de leur
        coordonee sur lecrant (interface) la fonction #mise_ajour c'est chargera de verifier les coligions ainsi que
        les action necessaire (manger, se reprodure, .....) qui tournera dans la boucle (500) qui veaut pour la moitié d'une
        journé"""

        """"A la fin de chaque journéé sera appelé les fonction de gestion de l'energie ainsi que le traitement
        des naissance"""
        self.execution = True
        pygame.mixer.music.load("Audio/animaux-de-la-savane-africaine-et-leurs-cris.wav")
        pygame.mixer.music.play()
        while self.execution:
            self.terrain.evolution()
            

if __name__ == "__main__":
    Simulation(1550,970).mainloop()
