# -*-coding:Utf-8 -*

"""Ce module contient la classe Labyrinthe."""

from random import randrange

from files.symbole import *
from files.commande import *


class Labyrinthe:

	"""Classe représentant un labyrinthe.
	Les attributs de cette classe sont :
	- nom
	- sortie			(les coordonnées de la porte de sortie)
	- grille			(un dictionnaire des objets présents sur la carte)
	- largeur			
	- hauteur	"""

	def __init__(self, carte):
		""" Constructeur de classe """
		self.nom = carte.nom
		self.sortie = ()
		self.grille = {}
		self.largeur = carte.largeur
		self.hauteur = carte.hauteur

	def __repr__(self):
		""" Méthode spéciale appelée par la fonction print """
		return "Labyrinthe en cours : {}".format(self.nom.capitalize())

			
	def afficher(self, liste_des_joueurs):			
		""" Retourne une liste de chaines de caractères, prêtes à être transmises aux clients."""
		# On créé un dictionnaire, dans lequel on place les représentations des différents symbôles
		# associées à leurs positions
		grille_affichage = {}
		for index, key in self.grille.items():
			grille_affichage[index] = key.repr_labyrinthe
		# On y ajoute les robots des différents joueurs
		for elt in liste_des_joueurs:
			grille_affichage[elt.robot] = elt.representation
		
		lignes = []		
		i = 0		
		while i < self.hauteur:
			# On va créer un élément par ligne dans la liste 'lignes'
			lignes.append([])			
			j = 0							
			while j < self.largeur:	
				# Chacun de ces éléments est une liste des symboles que l'on trouvera 
				# sur la ligne parcourue
				if (j, i) in grille_affichage:
					lignes[i].append(grille_affichage[j,i])				
				else:
					lignes[i].append(' ')						# A l'absence de symbole, on complète par un espace
				j += 1
			# Avant de l'envoyer, on transforme la liste de symboles 
			# contenus dans la ligne en une chaîne de caractères
			lignes[i] = "".join(lignes[i])
			i += 1
		return lignes	
			
	def choisir_emplacement_aleatoire(self, liste_des_joueurs):			
		""" Fonction choisissant une case libre aléaoire du labyrinthe pour y placer un robot."""
		i = 0
		j = 0
		while (i, j) in self.grille: 
			i = randrange(self.largeur)
			j = randrange(self.hauteur)
			if (i, j) in [elt.robot for elt in liste_des_joueurs]:
				i = 0
				j = 0
		return i, j

	def coordonnees_apres_deplacement(self, joueur, commande):
		""" Fonction permettant de calculer les futures coordonnées du robot."""
		X1 = joueur.robot[0]	# Coordonnées du robot
		Y1 = joueur.robot[1]
		X2 = int()				# Coordonnées du robot après déplacement
		Y2 = int()
		
		# Calcul des coordonnées du robot après déplacement		
		if commande == c_north:		
			(X2, Y2) = (X1, Y1-1)
		if commande == c_south:
			(X2, Y2) = (X1, Y1+1)
		if commande == c_east:
			(X2, Y2) = (X1+1, Y1)
		if commande == c_west:
			(X2, Y2) = (X1-1, Y1) 
		
		return (X2, Y2)
			
	def possibilite_deplacement(self, X2, Y2, liste_des_joueurs):
		""" Fonction permettant de vérifier la possibilité d'exécuter le déplacement calculé."""
		# On vérifie que les nouvelles coordonnées sont dans la carte
		if X2 >= 0 and X2 < self.largeur and Y2 >= 0 and Y2 < self.hauteur:
			deplacement_possible = True
		else:
			deplacement_possible = False
		# On vérifie qu'il n'y a pas d'obstacle.	
		if (X2,Y2) in self.grille:
			if self.grille[(X2,Y2)].obstacle:					
				deplacement_possible = False
		# On vérifie qu'il n'y a pas d'autre robot.
		if (X2,Y2) in [elt.robot for elt in liste_des_joueurs]:	
			deplacement_possible = False
		return deplacement_possible
	
	def coordonnees_porte(self, joueur, commande, direction):
		""" Fonction permettant de calculer les coordonnees de la porte à modifier."""
		X1 = joueur.robot[0]	# Coordonnées du robot
		Y1 = joueur.robot[1]
		X2 = int()				# Coordonnées de la porte à modifier
		Y2 = int()
		
		# Calcul des coordonnées de la porte à modifier		
		if direction == 'N':		
			(X2, Y2) = (X1, Y1-1)
		if direction == 'S':
			(X2, Y2) = (X1, Y1+1)
		if direction == 'E':
			(X2, Y2) = (X1+1, Y1)
		if direction == 'O' or direction == 'W':
			(X2, Y2) = (X1-1, Y1) 	
			
		return (X2, Y2)

	def possibilite_action(self, commande, X2, Y2):
		""" Fonction permettant de vérifier la possibilité d'exécuter le l'action souhaîtée."""
		action_possible = False
		if (X2,Y2) in self.grille:	
			# il faut un mur pour pouvoir le percer
			# il faut une porte pour pouvoir la murer
			if commande == c_percer and self.grille[(X2,Y2)] == s_mur \
			or commande == c_murer and self.grille[(X2,Y2)] == s_porte:	
				action_possible = True
		return action_possible
		
	def appliquer_action(self, commande, X2, Y2):
		""" Fonction permettant d'exécuter le l'action souhaîtée."""
		if commande == c_percer:			# Action : percer un mur
			self.grille[X2, Y2] = s_porte	
		if commande == c_murer:				# Action : murer une porte
			self.grille[X2, Y2] = s_mur
		