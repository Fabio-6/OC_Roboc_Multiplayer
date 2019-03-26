
# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du client.
Avant de l'exécuter, il faut démarrer le serveur (serveur.py) et y choisir une carte.

On lance ensuite ce programme une fois par joueur participant.

pour linux, ajouter
#!/usr/bin/python3.6
au début du fichier
"""

import os
import socket
import select
import re
import sys
import subprocess

from files.fonctions import *
from files.symbole import *
from files.commande import *
from files.joueur import Joueur
from files.carte import Carte
from files.labyrinthe import Labyrinthe

########################   MESSAGE D'ACCUEIL   #############################################

# Message d'acceuil
print('Bienvenue dans le client de Roboc - jeu de labyrinthe.')
print('Pensez à démarrer le serveur et sélectionnez une carte avant de commencer.\n')


########################   INITIALISATION DE LA CONNEXION   ###############################

# Instructions
print('Si le serveur est situé sur un autre ordinateur, entrez son adresse IP.')
print('Sinon, laissez ce champ vide.')

connexion_ok = False
while not connexion_ok:
	hote = input("Adresse : ")
	if hote == "":
		hote = "localhost"
	port = 12800

	# Connexion
	connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		connexion_avec_serveur.connect((hote, port))
	except ConnectionRefusedError:
		print("Démarrez le serveur avant d'essayer de vous connecter.")
	else:
		connexion_ok = True
			  
print("\nConnexion établie avec le serveur sur le port {}".format(port))

# Le serveur indique à quel joueur est attribué le client lancé
msg_recu = connexion_avec_serveur.recv(1024)
msg_recu = msg_recu.decode()
print("Il s'agit de la fenêtre de commande du joueur {}.".format(msg_recu))
print()

# On lance le script 'clientaffichage.py', qui ouvre une fenètre permettant au joueur de visualiser le labyrinthe


if sys.platform == 'win32':
	os.chdir('files')
	child = subprocess.Popen("start clientaffichage.py {}".format(hote), shell=True)
elif sys.platform == 'linux':
	os.chdir('files')
	child = subprocess.Popen("gnome-terminal -- './clientaffichage.py' {}".format(hote), shell=True)
else:
	input("Système d'exploitation non testé, possibilité de bug, désolé :(")
	os.chdir('files')
	child = subprocess.Popen("start clientaffichage.py {}".format(hote), shell=True)


		
		
########################   INITIALISATION DE LA PARTIE    ###############################		
		
# Envoi du nom du joueur
nom = input("Nom : ")
msg_a_envoyer = nom.encode()
connexion_avec_serveur.send(msg_a_envoyer)

# Envoi du symbôle représentant le joueur dans le labyrinthe
joueur_enregistre = False
representation = ""
while not joueur_enregistre:
	while representation == "":
		representation = input("Représentation : ")
		
		# on vérifie que le symbôle est compatible
		if len(representation) != 1:
			representation = ""
			print("Sélectionnez un seul caractère.")
			
	# On propose le symbôle au serveur
	msg_a_envoyer = representation.encode()
	connexion_avec_serveur.send(msg_a_envoyer)
	
	# Le serveur nous prévient si le symbôle a été correctement attribué.
	msg_recu = connexion_avec_serveur.recv(1024)
	msg_recu = msg_recu.decode()
	if msg_recu == "Joueur enregistre avec succes.":
		# Si tel est le cas, on informe le joueur
		joueur_enregistre = True	# et on passe à l'étape suivante
		print("\nJoueur enregistré.")
		print("Lorsque tous les joueurs sont prêts, entrez 'C' pour commencer la partie.")
	else:
		# Sinon, on retourne dans la boucle
		print('Représentation déjà utilisée.')
		representation = ""


########################   EN COURS DE PARTIE    ###############################

partie_en_cours = True
msg_a_envoyer = ""
while partie_en_cours:

	# Attente d'une nouvelle instruction
	while msg_a_envoyer == "":
		msg_a_envoyer = input('>')
	# que l'on envoie au serveur
	msg_a_envoyer = msg_a_envoyer.encode()
	connexion_avec_serveur.send(msg_a_envoyer)
	
	# On vérifie que la connexion est toujours effective
	try:
		msg_recu = connexion_avec_serveur.recv(1024)
	# Sinon, on se déconnecte
	except ConnectionAbortedError:
		partie_en_cours = False
		print('Erreur de connexion. Redémmarez le jeu pour une nouvelle partie.')
	# Le serveur renvoie un message après chaque instruction, pour nous signaler si elle est possible
	else:	
		msg_recu = msg_recu.decode()
		print(msg_recu)
	
	msg_a_envoyer = ""


########################  PARTIE TERMINEE    ###############################

# Message de fin
input('Au Revoir')
