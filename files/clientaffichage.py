
# -*-coding:Utf-8 -*
""" Ce fichier contient un client permettant l'affichage du labyrinthe pour chaque joueur.
Il n'y a pas besoin (il ne faut pas) lancer ce programme.
Il est exécuté automatiquement depuis le 'client.py'

pour linux, ajouter
#!/usr/bin/python3.6
au début du fichier
"""

import os
import socket
import select
import re
import sys

# Au démarrage, on récupère l'argument envoyé par 'client.py'
# Il permet de faire correspondre la fenêtre lancé au bon joueur
hote = sys.argv[1]
port = 12800

# Connexion au serveur
connexion_ok = False
while not connexion_ok:
	connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		connexion_avec_serveur.connect((hote, port))
	except ConnectionRefusedError:
		print("Démarrez le serveur avant d'essayer de vous connecter.")
	else:
		connexion_ok = True
			  
print("Connexion établie avec le serveur sur le port {}".format(port))

# On indique à quel joueur correspond la fenêtre ouverte
msg_recu = connexion_avec_serveur.recv(1024)
msg_recu = msg_recu.decode()
print("Il s'agit de la fenêtre d'affichage du joueur {}".format(msg_recu))

# Durant la partie, on affiche les messages envoyés par le serveur
partie_en_cours = True
while partie_en_cours:
	msg_recu = connexion_avec_serveur.recv(1024)
	msg_recu = msg_recu.decode()
	
	# Fin de partie, on quitte la boucle
	print(msg_recu, end='')
	if re.search(r"(relancer le programme.)$", msg_recu) is not None:
		partie_en_cours = False

input('Au Revoir.')
