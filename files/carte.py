# -*-coding:Utf-8 -*

"""Ce module contient la classe Carte."""


def creer_labyrinthe_depuis_chaine(chaine):
        """ Fonction transformant la chaîne de caractère contenue dans un fichier carte
        en un dictionnaire comportant la position des différents éléments du labyrinthe """
        labyrinthe = {}
        for i, ligne in enumerate(chaine.split('\n')):
                for j, lettre in enumerate(ligne):
                        labyrinthe[(j, i)] = lettre
        return labyrinthe
    

class Carte:
        """Objet de transition entre un fichier et un labyrinthe.
        ayant pour attributs
        - nom           (provenant du nom du fichier carte importé)
        - labyrinthe    (données provenant du fichier carte, sous formes de dictionnaire)
        - longueur      (largeur du labyrinthe)
        - hauteur       (hauteur du labyrinthe) """
    

        def __init__(self, nom, chaine):
                """ Constructeur de notre classe """
                self.nom = nom
                self.labyrinthe = creer_labyrinthe_depuis_chaine(chaine)
                self.largeur = len(chaine.split("\n")[0])
                self.hauteur = len(chaine.split("\n"))

        def __repr__(self):
                """ Méthode spéciale appelée lorsqu'on utilise la fonction print() """
                return "<Carte {}>".format(self.nom)

        def __lt__(self, objet_a_comparer):
                """ Méthode spéciale pour comparer '<' deux cartes """
                return self.largeur * self.hauteur < objet_a_comparer.largeur * objet_a_comparer.hauteur

        def afficher_carte(self):
                """ Méthode permettant de contrôler la cohérence des données
                du dictionnaire labyrinthe """
                print(self.labyrinthe)
	

