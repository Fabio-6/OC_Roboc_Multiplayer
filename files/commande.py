# -*-coding:Utf-8 -*

"""Ce module contient la classe Commande."""
import re

class Commande:
	"""Cette classe contient les les différentes commandes
	pouvant être entrées par les joueur
	Les attributs de cette classe sont :
	- nom				(nom utilisé dans la liste affichée dans l'aide)
	- info_breve		(en cours de partie, permet de dire quelle action a été menée précédemment)
	- info				(description de la commande, pour affichage dans l'aide)
	- regex				(expression régulière, permettant d'identifier la commande lors de sa saisie)
	"""

	liste = []
	
	def __init__(self, nom, info_breve, info, regex):
		""" Constructeur de notre classe """
		self.nom = nom
		self.info_breve = info_breve
		self.info = info
		self.regex = regex
		Commande.liste.append(self)

	def __repr__(self):
		""" Méthode spéciale affichant l'object """
		return "Commande {}".format(self.nom)


# Liste des commandes		

c_north = Commande('N', 'Aller vers le haut', 'Aller vers le haut. Peut être suivi par un nombre pour se déplacer de plusieurs cases (ex: N5)', r"^N[0-9]*$")
c_south = Commande('S', 'Aller vers le bas', 'Aller vers le bas.', r"^S[0-9]*$")
c_west = Commande('O', 'Aller vers la gauche', 'Aller vers la gauche.', r"^[OW][0-9]*$")
c_east = Commande('E', 'Aller vers la droite', 'Aller vers la droite.', r"^E[0-9]*$")

c_murer = Commande('M', "Murer une porte", "Murer une porte. Doit être suivit d'une direction (ex: MN pour murer la porte au Nord).", r"^M[NSWOE]$")
c_percer = Commande('P', "Percer une porte", "Percer une porte. Doit être suivit d'une direction (ex: PO pour percer une porte à l'Ouest).", r"^P[NSWOE]$")

c_help = Commande('H', "Afficher l'aide.", "Afficher l'aide.", r"^H(ELP)?$")
c_quit = Commande('Q', "Quitter.", "Quitter.", r"^Q$")

