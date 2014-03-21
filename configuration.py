#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

from commandline.parser import Parser

class Configuration:
    """
    Contient l'ensemble des paramètres nécessaires à l'exécution
    du programme.
    """

    def __init__(self):
        """Définit les valeurs par défaut"""

        self.source = None
        self.hote = "localhost"
        self.port = 21
        self.user = "anonymous"
        self.password = None

    def load_from_command_line(self, parser=Parser()):
        """Récupère les paramètres de la ligne de commande pour
        configurer l'application."""
        parser.parse()

        if parser.is_valide():
            parametres = parser.get_parametres()

            self.source = parametres["source"]
            self.hote = parametres["hote"]
            self.port = parametres["port"]
            self.user = parametres["user"]

            # Le mot de passe n'est valable que si un user est fourni.
            if parametres["user"] != "anonymous":
                self.password = parametres["password"]

        return self
