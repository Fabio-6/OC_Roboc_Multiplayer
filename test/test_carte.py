# -*-coding:Utf-8 -*

"""Ce fichier contient le test case pour tester les fonctions de la classe carte."""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath('..'))
from files.carte import *

class CarteTest(unittest.TestCase):

	"""Test case utilise pour tester les fonctions du fichier 'fonctions.py'."""
	
	def setUp(self):
		"""Initialisation des tests."""
		# On créé deux petites cartes, à l'aide de chaines de caractères
		self.chaine = "OOOO\nOX O\nO  U\nOOOO"
		self.carte_1 = Carte("Carte 1",self.chaine)
		self.chaine = "OOO\nOXO\nOOO"
		self.carte_2 = Carte("Carte 2",self.chaine)
	
	def test_creer_labyrinthe_depuis_chaine(self):
		"""Test le fonctionnement de la fonction 'creer_labyrinthe_depuis_chaine'."""
		# résultat supposé de la fonction 'creer_labyrinthe_depuis_chaine' utilisée lors de la création de la carte
		labyrinthe_ref = {(0,0): "O", (1,0): "O", (2,0): "O", (3,0): "O",
								  (0,1): "O", (1,1): "X", (2,1): " ", (3,1): "O",
								  (0,2): "O", (1,2): " ", (2,2): " ", (3,2): "U",
								  (0,3): "O", (1,3): "O", (2,3): "O", (3,3): "O"}
		# On vérifie que la grille de labyrinthe extraite de la carte correspond au labyrinthe à obtenir						  
		self.assertEqual(self.carte_1.labyrinthe, labyrinthe_ref)						  
		
	def test_dimensions(self):
		"""Test le fonctionnement du calcul des dimensions de la carte."""
		self.assertEqual(self.carte_1.largeur, 4)
		self.assertEqual(self.carte_1.hauteur, 4)					  
		
	def test_comparaison_lt(self):
		"""Test le fonctionnement de la méthode spécialle __lt__"""
		self.assertTrue(self.carte_2 < self.carte_1)
	


if __name__ == '__main__':
	unittest.main()
