# -*-coding:Utf-8 -*

"""Ce fichier contient le test case pour tester les fonctions.
A utiliser avec l'option unittest."""


import sys
import os
import unittest

sys.path.insert(0, os.path.abspath('..'))
from files.fonctions import *

class FonctionsTest(unittest.TestCase):

	"""Test case utilise pour tester les fonctions du fichier 'fonctions.py'."""


	def test_analyse_commande(self):
		"""Test le fonctionnement de la fonction 'analyse_commande'."""
		# On créé une commande
		commande = 'n10'
		cmd, chaine, instruction, argument = analyse_commande(commande)
		# On vérifie que les données extraites sont correctes
		self.assertIs(cmd, c_north)
		self.assertEqual(chaine, 'N10')
		self.assertIs(instruction, 'N')
		self.assertEqual(argument, '10')


if __name__ == '__main__':
    unittest.main()
