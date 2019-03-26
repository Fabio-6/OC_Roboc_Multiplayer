# -*-coding:Utf-8 -*

"""Ce module contient la classe Symbole."""

class Symbole:
	"""Cette classe contient les éléments présents dans le labyrinthe
	ainsi que leurs représentations. 
	Les attributs de cette classe sont :
	- nom
	- repr_carte		(le symbole utilisé sur le fichier 'carte')
	- repr_labyrinthe	(le symbole utilisé pour afficher le labyrinthe en cours de jeu)
	- robot				(s'agit-il d'un robot ? : oui si True)
	- obstacle			(empêche les robots de passer si True) """

	liste = []
	
	def __init__(self, nom, repr_carte, repr_labyrinthe, robot=False, obstacle=False):
		""" Constructeur de notre classe """
		self.nom = nom
		self.repr_carte = repr_carte
		self.repr_labyrinthe = repr_labyrinthe
		self.obstacle = obstacle
		self.robot = robot
		Symbole.liste.append(self)

	def __repr__(self):
		""" Méthode spéciale affichant l'object """
		return self.repr_labyrinthe

	def trouver_symbole(self, carte):
		""" Méthode permettant d'extraire la position des élément dans une carte """
		positions = []
		for cle, valeur in carte.labyrinthe.items():
			if valeur == self.repr_carte:
				positions.append(cle)
		return positions


# Symbôles de bases (d'autres symbôles sont créés par la suite, lors de l'enregistrement des joueurs)

s_sortie = Symbole('sortie','U','U')
s_mur= Symbole('mur','O','O', False, True)
s_porte = Symbole('porte','.','.')


