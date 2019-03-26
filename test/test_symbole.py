# -*-coding:Utf-8 -*

"""Ce fichier contient le test case pour tester les fonctions de la classe Labyrinthe.
A utiliser avec l'option unittest."""


import sys
import os
import unittest

sys.path.insert(0, os.path.abspath('..'))
from files.carte import *
from files.symbole import *

class SymboleTest(unittest.TestCase):

	"""Test case utilise pour tester les fonctions de la classe Labyrinthe."""

	def setUp(self):
		"""Initialisation des tests."""
		# On créé un labyrinthe, via une carte
		self.chaine = "OOOO\nOX.O\nO  U\nOOOO"
		self.carte = Carte("Carte",self.chaine)
			

	def test_trouver_symbole(self):
		"""Test le fonctionnement de la fonction 'trouver_symbole'."""
		# résultats supposés de la fonction 'trouver_symbole'
		liste_O = [(0,0), (1,0), (2,0), (3,0), (0,1), (3,1), (0,2), (0,3), (1,3), (2,3), (3,3)]
		liste_X = []
		
		# comparaison avec le résultat de la fonction
		self.assertEqual(s_mur.trouver_symbole(self.carte), liste_O)		  
			

if __name__ == '__main__':
    unittest.main()
