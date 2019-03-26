# -*-coding:Utf-8 -*

"""Ce fichier contient le test case pour tester les fonctions de la classe Joueur.
A utiliser avec l'option unittest."""


import sys
import os
import unittest

sys.path.insert(0, os.path.abspath('..'))
from files.joueur import *
from files.labyrinthe import *
from files.carte import *

class JoueurTest(unittest.TestCase):

	"""Test case utilise pour tester les fonctions de la classe Joueur."""

	def setUp(self):
		"""Initialisation des tests."""
		# On créé deux joueurs
		self.joueur_1 = Joueur(None)
		self.joueur_2 = Joueur(None)
		self.joueur_1.robot = (3,2)
		self.joueur_2.robot = (2,2)
		# On créé un labyrinthe, via une carte
		self.chaine = "OOOO\nOX O\nO  U\nOOOO"
		self.carte = Carte("Carte",self.chaine)
		self.labyrinthe = Labyrinthe(self.carte)
		self.labyrinthe.sortie = (3,2)
		
		
	def test_victoire(self):
		"""Test le fonctionnement de la fonction 'victoire'."""
		self.assertTrue(self.joueur_1.victoire(self.labyrinthe))
		self.assertFalse(self.joueur_2.victoire(self.labyrinthe))
		
		
	def test_supprimer(self):
		"""Test le fonctionnement de la fonction 'supprimer'."""
		self.joueur_2.supprimer()						# suppression du joueur
		self.assertNotIn(self.joueur_2, Joueur.liste)	# on vérifie que le joueur n'est plus dans la liste




if __name__ == '__main__':
    unittest.main()
