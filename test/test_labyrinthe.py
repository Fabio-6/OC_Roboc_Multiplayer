# -*-coding:Utf-8 -*

"""Ce fichier contient le test case pour tester les fonctions de la classe Labyrinthe.
A utiliser avec l'option unittest."""


import sys
import os
import unittest
from random import randrange

sys.path.insert(0, os.path.abspath('..'))
from files.joueur import *
from files.labyrinthe import *
from files.carte import *
from files.commande import *

class LabyrintheTest(unittest.TestCase):

	"""Test case utilise pour tester les fonctions de la classe Labyrinthe."""

	def setUp(self):
		"""Initialisation des tests."""
		# On créé un labyrinthe, via une carte
		self.chaine = "OOOO\nOX.O\nO  U\nOOOO"
		self.carte = Carte("Carte",self.chaine)
		self.labyrinthe = Labyrinthe(self.carte)		
		for symb in Symbole.liste:
			for elt in symb.trouver_symbole(self.carte):
				self.labyrinthe.grille[elt] = symb
		# On créé un joueur		
		self.joueur_1 = Joueur(None)
		self.joueur_1.robot = (3,2)
		
	def test_afficher(self):
		"""Test le fonctionnement de la fonction 'afficher'."""
		liste = ["OOOO", "O .O", "O  U", "OOOO"]				# résultat supposé de la fonction 'afficher'
		self.assertEqual(self.labyrinthe.afficher([]), liste)	# comparaison avec le résultat de la fonction
		
	def test_choisir_emplacement_aleatoire(self):
		"""Test le fonctionnement de la fonction 'choisir_emplacement_aleatoire'."""
		i, j = self.labyrinthe.choisir_emplacement_aleatoire([])	# exécution de la fonction
		emplacements_libres = [(1,1), (2,1), (1,2), (2,2)]			# liste des résultats possibles
		self.assertIn((i, j), emplacements_libres)

		
	def test_coordonnees_apres_deplacement(self):
		"""Test le fonctionnement de la fonction 'coordonnees_apres_deplacement'."""
		X2, Y2 = self.labyrinthe.coordonnees_apres_deplacement(self.joueur_1, c_north)	# exécution de la fonction
		self.assertEqual((X2, Y2), (3,1))												# comparaison avec le résultat souhaité
		X2, Y2 = self.labyrinthe.coordonnees_apres_deplacement(self.joueur_1, c_west)	# ... x4
		self.assertEqual((X2, Y2), (2,2))
		X2, Y2 = self.labyrinthe.coordonnees_apres_deplacement(self.joueur_1, c_south)
		self.assertEqual((X2, Y2), (3,3))
		X2, Y2 = self.labyrinthe.coordonnees_apres_deplacement(self.joueur_1, c_east)
		self.assertEqual((X2, Y2), (4,2))

		
	def test_possibilite_deplacement(self):
		"""Test le fonctionnement de la fonction 'possibilite_deplacement'."""
		self.assertFalse(self.labyrinthe.possibilite_deplacement(3, 1, []))	# on ne doit pas pouvoir se déplacer sur un obstable
		self.assertTrue(self.labyrinthe.possibilite_deplacement(2, 2, []))	# on doit pouvoir se déplacer ailleurs

		
	def test_coordonnees_porte(self):
		"""Test le fonctionnement de la fonction 'coordonnees_porte'."""
		X2, Y2 = self.labyrinthe.coordonnees_porte(self.joueur_1, c_percer, 'N')	# exécution de la fonction
		self.assertEqual((X2, Y2), (3,1))											# comparaison avec le résultat souhaité
		X2, Y2 = self.labyrinthe.coordonnees_porte(self.joueur_1, c_murer, 'O')		# ... x4
		self.assertEqual((X2, Y2), (2,2))
		X2, Y2 = self.labyrinthe.coordonnees_porte(self.joueur_1, c_percer, 'S')
		self.assertEqual((X2, Y2), (3,3))
		X2, Y2 = self.labyrinthe.coordonnees_porte(self.joueur_1, c_murer, 'E')
		self.assertEqual((X2, Y2), (4,2))

		
	def test_possibilite_action(self):
		"""Test le fonctionnement de la fonction 'possibilite_action'."""
		self.assertTrue(self.labyrinthe.possibilite_action(c_percer, 3, 1))		# on doit pouvoir percer un mur
		self.assertFalse(self.labyrinthe.possibilite_action(c_murer, 3, 1))		# on ne doit pas pouvoir murer un mur
		self.assertTrue(self.labyrinthe.possibilite_action(c_murer, 2, 1))		# on doit pouvoir murer une porte
		self.assertFalse(self.labyrinthe.possibilite_action(c_percer, 2, 1))	# on ne doit pas pouvoir percer une porte

		
	def test_appliquer_action(self):
		"""Test le fonctionnement de la fonction 'appliquer_action'."""
		self.labyrinthe.appliquer_action(c_percer, 3, 1)			# exécution de la fonction
		self.assertEqual(self.labyrinthe.grille[(3, 1)], s_porte)	# comparaison avec le résultat souhaité
		
		self.labyrinthe.appliquer_action(c_murer, 2, 1)				# exécution de la fonction				
		self.assertEqual(self.labyrinthe.grille[(2, 1)], s_mur)		# comparaison avec le résultat souhaité
		
		

if __name__ == '__main__':
    unittest.main()
