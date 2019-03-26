# -*-coding:Utf-8 -*

"""Ce module contient la classe Joueur."""

class Joueur:
	"""Cette classe contient les éléments attribués aux différents joueurs.
	Les attributs de cette classe sont :
	- nom					nom du joueur, qu'il choisira en début de partie
	- numero				numéro du joueur, attribué automatiquement lors de la création d'un joueur
	- connexion_commande	connexion communiquant avec le 1er client du joueur, lui permettant d'entrer des instructions
	- connexion_affichage	connexion communiquant avec le 2nd client du joueur, lui permettant d'afficher le labyrinthe
	- etape_connexion		numero permettant au serveur de savoir que faire des instructions émises par le client
								etape_connexion == 0		le serveur attent le nom du joueur
								etape_connexion == 1		le serveur attent le symbôle représentant le joueur
								etape_connexion == 2		le joueur est prêt à commencer la partie, en attente d'une position de départ
								etape_connexion == 3		le joueur a reçu sa position de départ
	- commande_enregistree	dans le cas ou l'on demande plusieurs déplacement ('N10', 'E5' ...), la commande est enregistrée pour le prochain tour
	- robot					position du robot du joueur dans le labyrinthe
	- representation		symbôle représentant le joueur dans le labyrinthe, qu'il choisira en début de partie
	- connexion

	"""
	objets_crees = 0	# variable incrémentée à la création de chaque joueur, afin de lui attribué un numéro
	liste = []			# liste des joueurs, remplie automatiquement
	
	def __init__(self, connexion):
		""" Constructeur de notre classe """
		self.connexion_commande = connexion
		self.connexion_affichage = None
		self.etape_connexion = 0
		self.commande_enregistree = None
		self.robot = ()
		self.representation = "X"
		Joueur.objets_crees += 1
		self.nom = "Joueur {}".format(Joueur.objets_crees)
		self.numero = Joueur.objets_crees
		Joueur.liste.append(self)
		

	def __repr__(self):
		"""Méthode spéciale affichant l'object """
		return self.nom
		
	def supprimer(self):
		"""Méthode servant à supprimer un joueur."""		
		if self.connexion_commande is not None:	# On ferme d'abord les connexions liées au joueur
			self.connexion_commande.close()		
		if self.connexion_affichage is not None:		
			self.connexion_affichage.close()
		Joueur.liste.remove(self)				# On supprime le joueur de la liste
		del self								# Enfin, on supprime l'instance

	def envoyer_message(self, message):
		"""Envoyer un message et vérifie qu'il n'y a pas d'erreur."""
		message = message + "\n"	# Saut de ligne pour distinguer plusieurs messages envoyés consécutivement
		message = message.encode()	
		try:
			self.connexion_affichage.send(message)
		except ConnectionResetError:
			print("Problème de connecxon au client d'affichage du joueur {}.".format(self.numero))
			# En cas de problème de connexion, on avertit les autres joueurs
			for elt in Joueur.liste:
				if elt != self:
					elt.envoyer_message("Probleme de connecxon au client d'affichage du joueur {}.".format(self.numero))
			# Puis on efface le joueur
			self.supprimer()
			
		
	def victoire(self, labyrinthe):
		""" Fonction vérifiant si l'on a atteint la sortie """
		return self.robot == labyrinthe.sortie		
			
			
			