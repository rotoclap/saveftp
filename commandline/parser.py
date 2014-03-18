#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

import argparse

from commandline.actions import PortAction

class Parser:
    """
    Valide et renvoie les paramètres fournis en ligne de commande.
    """
    def __init__(self):
        """Configure le parseur."""

        self.parser = argparse.ArgumentParser(
                prog="SaveFTP",
                description="""
Sauvegarde une arborescence dans une archive zip, puis la transfère 
par FTP sur un serveur distant.
"""
        )
        self.parser.add_argument("source", 
                type=str, 
                help="""
L'aborescence à sauvegarder.
"""
        )
        self.parser.add_argument("hote", 
                type=str, 
                help="""
L'hôte vers lequel sera transférer l'archive. Cela doit 
être une IP ou un nom qui sera résolu comme tel.
"""
        )
        self.parser.add_argument("--port", 
                metavar="NUMERO", 
                dest="port",
                type=int,
                default=21, 
                action=PortAction,
                help="""
Le numéro de port (1-65535) pour la connexion vers l'hôte.
S'il n'est pas spécifié, le port 21 sera utilisé.
"""
        )
        self.parser.add_argument("-u", "--user", 
                dest="user", 
                type=str,
                default="anonymous",
                help="""
Nom d'utilisateur pour l'identification sur le serveur FTP. En son
absence, la connexion se fera en anonyme.
"""
        )

        self.parser.add_argument("-p", "--password", 
                dest="password", 
                type=str,
                help="""
Mot de passe de l'utilisateur servant à l'identification sur 
le serveur FTP.
"""
        )

        self.arguments = None

    def parse(self):
        """Extrait les paramètres de la ligne de commande"""
        self.arguments = self.parser.parse_args()

    def is_valide(self):
        """Renvoit vrai si les arguments extraits sont valides."""
        if self.arguments:
            return True
        else:
            return False

    def get_parametres(self):
        """Renvoie les paramètres dans un dictionnaire."""
        return {
            "source":self.arguments.source,
            "hote":self.arguments.hote,
            "port":self.arguments.port,
            "user":self.arguments.user,
            "password":self.arguments.password
        }
