
# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du jeu.
Exécutez-le avec Python pour lancer le jeu.

Après avoir sélectionné la carte, exécutez un client (client.py) pour chaque joueur participant.

pour linux, ajouter
#!/usr/bin/python3.6
au début du fichier
"""

import os
import socket
import select
import re

from files.fonctions import *
from files.symbole import *
from files.commande import *
from files.joueur import Joueur
from files.carte import Carte
from files.labyrinthe import Labyrinthe

########################   SELECTION DE LA CARTE   #############################################


# Message d'acceuil
print('Bienvenue dans le serveur de Roboc - jeu de labyrinthe.\n')
print('Veuillez sélectionner une carte avant de lancer un client pour chaque joueur.')

# On charge les cartes existantes
cartes = []
for nom_fichier in os.listdir("cartes"):
	if nom_fichier.endswith(".txt"):
		chemin = os.path.join("cartes", nom_fichier)
		nom_carte = nom_fichier[:-4].lower()
		with open(chemin, "r") as fichier:
			contenu = fichier.read()
		carte = Carte(nom_carte,contenu)
		cartes.append(carte)
		
# On tri les cartes par taille
cartes.sort()
		
# On affiche les cartes existantes
print("Labyrinthes existants :")
for i, carte in enumerate(cartes):
	print("	 {} - {} (taille : {} x {})".format(
		i + 1, carte.nom.capitalize(), carte.largeur, carte.hauteur))

# Sélection de la carte
num_carte = choisir_nb_entre_un_et(len(cartes), "\nEntrez un numéro de labyrinthe pour commencer une nouvelle partie : ") - 1
# Chargement des données de la carte dans l'objet labyrinthe
labyrinthe = Labyrinthe(cartes[num_carte])
labyrinthe.sortie = s_sortie.trouver_symbole(cartes[num_carte])[0]
for symb in Symbole.liste:
	for elt in symb.trouver_symbole(cartes[num_carte]):
		labyrinthe.grille[elt] = symb
			
# Message
print("Carte {} '{}' chargée.".format(num_carte + 1, cartes[num_carte].nom.capitalize()))



########################   MISE EN PLACE DES CONNEXIONS    #########################################

# Connexion serveur
hote = ''
port = 12800
connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("On attend les clients.")

# Initialisation de quelques variables
serveur_lance = True			# Booléen permettant de savoir s'il faut communiquer avec les clients
debut_partie = False			# Tant que debut_partie == False, on attend de nouveaux joueurs
fin_de_partie = False			# Lorsque fin_de_partie == True, on quitte la partie
clients_connectes = []			# liste des clients à écouter
nb_connexions = 0				# Compte les clients pour les associer aux différents joueurs
tour_du_joueur_numero = 0		# Permet de savoir qui doit effectuer une action

while serveur_lance and not fin_de_partie:
	
	# On attend que les clients se connectent
	# (chaque joueur possède 2 client : un pour entrer les instructions, l'autre pour visualiser le jeu)
	if not debut_partie:
		connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)
	   
		for connexion in connexions_demandees:
			nb_connexions += 1
			# On accepte les connexions des clients
			connexion_avec_client, infos_connexion = connexion.accept()
			
			# On ajoute les sockets connectés à la liste des joueurs
			if nb_connexions % 2 == 1:
				# Un socket sur deux (client pour entrer les instructions) est associé à un nouveau joueur
				joueur = Joueur(connexion_avec_client)
				msg = str(joueur.numero).encode()
				connexion_avec_client.send(msg)
			else:
				# Le socket suivant (client pour visualiser le jeu) est attribué au joueur créé précédemment 
				Joueur.liste[-1].connexion_affichage = connexion_avec_client
				msg = str(joueur.numero).encode()
				connexion_avec_client.send(msg)
			print("Le client n°{} (Joueur {}) s'est connecté.".format(nb_connexions, joueur.numero))
			
	
	# On identifie la liste des clients à lire
	clients_connectes = [elt.connexion_commande for elt in Joueur.liste]
	clients_a_lire = []
	try:
		clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
	except select.error:
		pass	  
	else:
		# On parcourt la liste des clients à lire
		for client in clients_a_lire:
			joueur = [elt for elt in Joueur.liste if elt.connexion_commande == client][0] # ligne désignant le joueur concerné par la connexion entrante
			try:
				msg_recu = client.recv(1024)
				
			# Si un client se déconnecte
			except ConnectionResetError:
				msg = "Le joueur {}, {} s'est déconnecté.".format(joueur.numero, joueur.nom)	# Affichage d'un message d'alerte
				print(msg)																		
				for joueur_a_contacter in Joueur.liste:											# Envoi du message aux autres joueurs
					joueur_a_contacter.envoyer_message(msg)										
				joueur.supprimer()											# Fermeture des connexions et suppression de l'objet Joueur
			
			# Sinon, on traite le message reçu
			else:
				msg_recu = msg_recu.decode()
				
				
				
				########################   ENREGISTREMENT DES JOUEURS    #########################################				
			
				# Les 1ers messages reçus permettent de créer le profil des joueurs (nom, représentation)
				if not debut_partie:				
					
					# Réception du nom du joueur
					if joueur.etape_connexion == 0:			# etape_connexion == 0 : joueur connecté non nommé
						joueur.nom = msg_recu.capitalize()
						joueur.etape_connexion += 1
					
					# Réception du symbôle choisi par le joueur					
					elif joueur.etape_connexion == 1:		# etape_connexion == 1 : joueur nommé, sans symbole attribué
						if msg_recu in [elt.repr_labyrinthe for elt in Symbole.liste]:	# On vérifie que le symbole n'est pas déjà pris
							client.send(b"Representation deja utilisee.")
						else:
							# Enregistrement du symbôle
							joueur.representation = msg_recu							
							symbole = Symbole(joueur.nom + " (joueur " + str(joueur.numero) + ")", "", joueur.representation, True, True)
							client.send(b"Joueur enregistre avec succes.")
							
							# On annonce que le joueur est prêt
							msg = "\nJoueur {} enregistre.".format(joueur.numero)
							print(msg)					
							for joueur_a_contacter in Joueur.liste:
								joueur_a_contacter.envoyer_message(msg)
							joueur.etape_connexion += 1
							
							# Et on affiche la liste des joueurs prêts						
							for joueur_a_contacter in Joueur.liste:
								joueur_a_contacter.envoyer_message("Joueurs prets :")
								for joueur_present in Joueur.liste:
									if joueur_present.etape_connexion >= 2:
										msg = "  - '{}' : {} (Joueur {})".format(joueur_present.representation, joueur_present.nom, joueur_present.numero) 									
										joueur_a_contacter.envoyer_message(msg)						
							
					
					# Attente du début de partie
					elif joueur.etape_connexion == 2:	# etape_connexion == 2 : joueur prêt, sans position de départ attribuée
						if not msg_recu.upper() == 'C':
							client.send(b"Pour commencer la partie, tapez 'C'.")
						else:
							debut_partie = True
							print('Début de partie.')
							client.send(b"La partie commence.")							
							
							
							########################   INITIALISATION DE LA PARTIE    #########################################						
							
							# Début de la partie						
							for joueur_a_initialiser in Joueur.liste:
								# On supprime les joueurs pas prêts			
								if joueur_a_initialiser.etape_connexion < 2:
									print("Déconnexion du joueur {}.".format(joueur_a_initialiser.numero))
									joueur_a_initialiser.supprimer()
									
								# On attribue une position de départ dans le labyrinthe aux joueurs restant
								elif joueur_a_initialiser.etape_connexion == 2:
									i, j = labyrinthe.choisir_emplacement_aleatoire(Joueur.liste)
									joueur_a_initialiser.robot = (i, j)
									joueur_a_initialiser.etape_connexion += 1
							
							# Premier affichage du labyrinthe						
							for joueur_a_contacter in Joueur.liste:
								i = 0
								while i < 10:
									joueur_a_contacter.envoyer_message(" ")					# quelques sauts de ligne pour aérer l'affichage
									i += 1							
								joueur_a_contacter.envoyer_message("La partie demarre.\n")	# message "La partie demarre."						
								for ligne in labyrinthe.afficher(Joueur.liste):				
									joueur_a_contacter.envoyer_message(ligne)				# affichage du labyrinthe
								# Indication du joueur dont c'est le tour
								joueur_a_contacter.envoyer_message("\nC'est au tour de {} (Joueur {}).\n".format(Joueur.liste[tour_du_joueur_numero].nom,
																									Joueur.liste[tour_du_joueur_numero].numero))
					
					
				########################   PARTIE EN COURS    #########################################		

				# Echanges avec les clients en cours de partie
				elif not fin_de_partie:
					# On analise la commande envoyée par le client
					cmd, chaine, instruction, argument = analyse_commande(msg_recu)
					
					# Si la commande n'est pas valide, on en redemande une
					if cmd is None:
						client.send(b"Instruction inconnue. Entrez H pour afficher les instructions.")				
					
					# Si la commande est 'Q', on supprime le joueur					
					if cmd is c_quit:
						client.send(b"Au revoir.")	
						msg = "{} (Joueur {})) declare forfait, et quitte le jeu.".format(joueur.nom, joueur.numero)
						for joueur_a_contacter in Joueur.liste:
							joueur_a_contacter.envoyer_message(msg)
						joueur.supprimer()
					
					# Si la commande est 'H', on envoie les instructions					
					if cmd is c_help:
						client.send(b"Affichage de l'aide.\n")						
						# Liste des symbôles
						joueur.envoyer_message("\nLes differents symboles sont :")
						for elt in Symbole.liste:
							joueur.envoyer_message("	 {} : {}".format(elt.repr_labyrinthe, elt.nom))						
						# Règle du jeu
						joueur.envoyer_message("\nVous devez deplacer le robot jusqu'a la sortie.\n")						
						# Liste des commandes
						joueur.envoyer_message("Pour cela, les differentes commandes sont :")
						for elt in Commande.liste:
							joueur.envoyer_message("	 {} : {}".format(elt.nom, elt.info))
							
					# Si la commande est une commande d'action				
					if cmd in [c_south, c_west, c_east, c_north, c_murer, c_percer]:
					
						# on vérifie que le joueur est celui dont c'est le tour
						if tour_du_joueur_numero != Joueur.liste.index(joueur):
							client.send(b"Veuillez attendre votre tour.\n")
							
						# on vérifie que le joueur n'a pas déjà une action de prévue
						elif joueur.commande_enregistree is not None:
							msg = "Vous avez deja une instruction en attente ({}).\n".format(joueur.commande_enregistree)
							msg = msg.encode()
							client.send(msg)
						else:
						
							# Si l'action consiste à percer ou murer une porte
							if cmd in [c_murer, c_percer]:
								# On vérifie la possibilité de l'action
								(X2, Y2) = labyrinthe.coordonnees_porte(joueur, cmd, argument)
								if not labyrinthe.possibilite_action(cmd, X2, Y2):
									client.send(b"Action impossible. Entrez une nouvelle instruction.")
								# Si possible, on l'exécute
								else:
									labyrinthe.appliquer_action(cmd, X2, Y2)
									
									# et on affiche le labyrinthe dans son nouvel état
									for joueur_a_contacter in Joueur.liste:
										i = 0
										while i < 10:
											joueur_a_contacter.envoyer_message(" ")		# quelques sauts de ligne pour aérer l'affichage
											i += 1
										# on indique la dernière action effectuée
										joueur_a_contacter.envoyer_message("{} (Joueur {}) effectue '{}'.\n".format(joueur.nom, joueur.numero, cmd.info_breve))
										for ligne in labyrinthe.afficher(Joueur.liste):
											joueur_a_contacter.envoyer_message(ligne)	# affichage du labyrinthe
									
									client.send(b"Action effectuee.")
									
									# On passe au joueur suivant
									tour_du_joueur_numero += 1
									if tour_du_joueur_numero >= len(Joueur.liste):
										tour_du_joueur_numero = 0
									# et on prévient les joueurs
									for joueur_a_contacter in Joueur.liste:
										joueur_a_contacter.envoyer_message("\nC'est au tour de {} (Joueur {}).\n".format(Joueur.liste[tour_du_joueur_numero].nom,
																											Joueur.liste[tour_du_joueur_numero].numero))
							# Si l'action est un déplacement
							if cmd in [c_south, c_west, c_east, c_north]:
								# On vérifie la possibilité de l'action
								(X2, Y2) = labyrinthe.coordonnees_apres_deplacement(joueur, cmd)
								if not labyrinthe.possibilite_deplacement(X2, Y2, Joueur.liste):
									client.send(b"Deplacement impossible. Entrez une nouvelle instruction.")
								# Si possible, on l'exécute
								else:
									joueur.robot = X2, Y2
									
									# et on affiche le labyrinthe dans son nouvel état
									for joueur_a_contacter in Joueur.liste:
										i = 0
										while i < 10:
											joueur_a_contacter.envoyer_message(" ")		# quelques sauts de ligne pour aérer l'affichage
											i += 1
										# on indique la dernière action effectuée
										joueur_a_contacter.envoyer_message("{} (Joueur {}) effectue '{}'.\n".format(joueur.nom, joueur.numero, cmd.info_breve))
										for ligne in labyrinthe.afficher(Joueur.liste):
											joueur_a_contacter.envoyer_message(ligne)	# affichage du labyrinthe
											
									client.send(b"Deplacement effectue.")
									
									# On vérifie si cette action entraine la victoire du joueur
									if not joueur.victoire(labyrinthe):
									
										# Si non, on vérifie s'il s'agissait d'un déplacement de plusieurs cases
										try:
											argument = int(argument)
										except ValueError:
											argument = 0

										# dans ce cas, on sauvegarde la commande pour le prochain tour	
										if argument >= 2:
											argument -= 1
											joueur.commande_enregistree = instruction + str(argument)
										else:
											joueur.commande_enregistree = None	# sinon, non

										# On passe au joueur suivant
										tour_du_joueur_numero += 1
										if tour_du_joueur_numero >= len(Joueur.liste):
											tour_du_joueur_numero = 0
										# et on prévient les joueurs
										for joueur_a_contacter in Joueur.liste:
											joueur_a_contacter.envoyer_message("\nC'est au tour de {} (Joueur {}).\n".format(Joueur.liste[tour_du_joueur_numero].nom,
																												Joueur.liste[tour_du_joueur_numero].numero))
									# Si l'action entraine la victoire du joueur, on en informe les joueurs																			
									else:
										fin_de_partie = True	# Et on quitte la boucle
										msg = "\n{} (Joueur {})) a trouve la sortie et gagne la partie.".format(joueur.nom, joueur.numero)
										print(msg)
										for joueur_a_contacter in Joueur.liste:											
											joueur_a_contacter.envoyer_message(msg)
										msg = "\n\n\n\n\n\nPour rejouer, relancer le programme."											
										for joueur_a_contacter in Joueur.liste:
											joueur_a_contacter.envoyer_message(msg)											
	
	########################   EN DEHORS DES ECHANGES SYNCHRONISES CLIENT / SERVEUR    #########################################
	
	# Si il n'y a plus de joueurs, on quitte la partie
	if debut_partie and len(Joueur.liste) == 0:
		fin_de_partie = True
		print("Tous les joueurs sont partis.")
		
	# Dans le cas où un joueur a enregistré une commande, on n'attend pas qu'il en envoie une nouvelle.	
	# On traite donc cette commande en dehors de la précédente boucle.
	# Il s'agit toutefois d'un code similaire à ce que l'on a vu au dessus dans le paragraphe "Si l'action est un déplacement"
	
	if debut_partie and not fin_de_partie :
		# On vérifie si le joueur dont c'est le tour a une instruction enregistrée
		joueur_en_cours = Joueur.liste[tour_du_joueur_numero]
		if joueur_en_cours.commande_enregistree is not None:
			# Si oui, on la décode
			cmd, chaine, instruction, argument = analyse_commande(joueur_en_cours.commande_enregistree)
			# On teste sa possibilité
			(X2, Y2) = labyrinthe.coordonnees_apres_deplacement(joueur_en_cours, cmd)
			if not labyrinthe.possibilite_deplacement(X2, Y2, Joueur.liste):
				# Si l'action est impossible, on l'annule
				joueur_en_cours.envoyer_message("Deplacement impossible. Entrez une nouvelle instruction.")
				joueur_en_cours.commande_enregistree = None
			else:
				# Sinon, on l'exécute
				joueur_en_cours.robot = X2, Y2
				
				# et on affiche le labyrinthe dans son nouvel état
				for joueur_a_contacter in Joueur.liste:
					i = 0
					while i < 10:
						joueur_a_contacter.envoyer_message(" ")		# quelques sauts de ligne pour aérer l'affichage
						i += 1
					# on indique la dernière action effectuée
					joueur_a_contacter.envoyer_message("{} (Joueur {}) effectue '{}'.\n".format(joueur_en_cours.nom, joueur_en_cours.numero, cmd.info_breve))
					for ligne in labyrinthe.afficher(Joueur.liste):
						joueur_a_contacter.envoyer_message(ligne)	# affichage du labyrinthe
				
				# On vérifie si cette action entraine la victoire du joueur
				if not joueur_en_cours.victoire(labyrinthe):
					
					# Si non, on vérifie s'il s'agissait d'un déplacement de plusieurs cases
					try:
						argument = int(argument)
					except ValueError:
						argument = 0
					# dans ce cas, on sauvegarde la commande pour le prochain tour	
					if argument >= 2:
						argument -= 1
						joueur_en_cours.commande_enregistree = instruction + str(argument)
					else:
						joueur_en_cours.commande_enregistree = None		# sinon, non

					# On passe au joueur suivant
					tour_du_joueur_numero += 1
					if tour_du_joueur_numero >= len(Joueur.liste):
						tour_du_joueur_numero = 0
					# et on prévient les joueurs
					for joueur_a_contacter in Joueur.liste:
						joueur_a_contacter.envoyer_message("\nC'est au tour de {} (Joueur {}).\n".format(Joueur.liste[tour_du_joueur_numero].nom,
																							Joueur.liste[tour_du_joueur_numero].numero))	
				# Si l'action entraine la victoire du joueur, on en informe les joueurs	
				else:
					fin_de_partie = True		# et on quitte la boucle
					msg = "\n{} (Joueur {})) a trouve la sortie et gagne la partie.".format(joueur_en_cours.nom, joueur_en_cours.numero)
					print(msg)
					for joueur_a_contacter in Joueur.liste:											
						joueur_a_contacter.envoyer_message(msg)
					msg = "\n\n\n\n\n\nPour rejouer, relancer le programme."											
					for joueur_a_contacter in Joueur.liste:
						joueur_a_contacter.envoyer_message(msg)			



########################   FIN DE LA PARTIE    #########################################	

# On supprime les joueurs et déconnecte les clients
print("Fermeture des connexions.")
for joueur in Joueur.liste:
	joueur.supprimer()

# On ferme la connexion principale
connexion_principale.close()

# Message de fin
input('\nAu revoir ! Pour rejouer, relancer le programme.')
