# -*-coding:Utf-8 -*

""" Fonctions utilisées par le programme

	On y retrouve des fonctions pour communiquer avec les utilisateurs
		- choisir_nb_entre_un_et		permet de choisir un nombre
		- question_oui_non				pose une question attendant une réponse en oui / non
		- analyse_commande				traite l'instruction utilisateur afin de déterminer l'action demandée

 """

from files.commande import *


###     Fonctions pour communiquer avec l'utilisateur     ###

def choisir_nb_entre_un_et(nombre, texte):
	""" Fonction demandant à l'utilisateur d'entrer un nombre entre 1 et X """
	n = 0
	while n == 0:
		try:
			n = int(input(texte))
			assert n >= 1 and n <= nombre
		except ValueError:
			print('Vous devez choisir un nombre')
			n = 0
		except AssertionError:
			print('Sélectionnez un numéro valide (entre 1 et {})'.format(nombre))
			n = 0
	return n


def question_oui_non(question):
	""" Fonction demandant à l'utilisateur de répondre par oui ou non (O/N)  """
	question += '(O/N)'
	reponse = str()
	while reponse == '':
		reponse = input(question)
		if reponse.lower() != 'o' and reponse.lower() != 'n':
			reponse = ''
	return reponse.lower() == 'o'



def analyse_commande(commande):
	"""Fonction récupérant les instructions utilisateur et vérifiant leur existence."""
	chaine = commande.upper()
	commande_ok = False
	cmd = None
	instruction = ""
	argument = ""
	for elt in Commande.liste:
		if re.match(elt.regex, chaine):
			commande_ok = True
			cmd = elt
			instruction = chaine[0]
			argument = chaine[1:]
	return cmd, chaine, instruction, argument



def envoyer_message_a_tous(message, liste_des_joueurs):
	"""Envoye un message à tous les joueurs et vérifie qu'il n'y a pas d'erreur."""
	for joueur in liste_des_joueurs:
		joueur.envoyer_message(message)