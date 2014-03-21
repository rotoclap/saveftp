#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

import ftplib
import os
import tempfile
import zipfile

from configuration import Configuration

class SaveFTP():
    """Sauvegarde d'une arborescence dans une archive zip, et
    transfert sur un serveur via FTP.
    """

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)

        return cls._instance

    def __init__(self):
        self.fichiers = list()
        self.fichiers_archive = list()
        self.archive = None
        self.configuration = None
   
    def load_configuration(self, configuration):
        """Configuration de l'application"""

        configuration.load_from_command_line()
        self.configuration = configuration

        return self

    def build_liste_fichiers(self):
        """Genere la liste des fichiers a inclure dans l'archive.

        La methode genere deux listes : 
        * fichiers contient l'arborescence complete de chaque fichier
        * fichiers_archive contient l'arborescence qu'aura le fichier
          dans l'archive.

        Pour cette seconde liste, on prend l'arboresence complete et
        on supprime tout jusqu'au repertoire de depart (non inclus)
        tel qu'il a ete fourni dans la ligne de commande. Ex :

        Avec "--source=d:/repertoire/repertoire/a_archiver",
        l'arborescence de la seconde liste demarrera par
        "a_archiver\\..."
        """
        
        self._get_liste_fichiers(self.configuration.source)
        
        # Calcul de ce qu'on doit retirer de l'arborescence pour
        # générer la liste fichiers_archive
        longueur_arborescence = len(self.configuration.source)
        longueur_base_repertoire = \
            len(os.path.basename(self.configuration.source))
        longueur = longueur_arborescence - longueur_base_repertoire

        for fichier in self.fichiers:
            self.fichiers_archive.append(fichier[longueur:])

        return self

    def _get_liste_fichiers(self, path):
        for fichier in os.listdir(path):
            if os.path.isdir(path + "\\" + fichier):
                self._get_liste_fichiers(path + "\\" + fichier)
            else:
                self.fichiers.append(path + "\\" + fichier)

    def build_archive(self):
        self.archive = tempfile.SpooledTemporaryFile()

        with zipfile.ZipFile(
                self.archive,
                mode="w",
                compression=zipfile.ZIP_DEFLATED
                ) as fichier_zip:
            for i, fichier in enumerate(self.fichiers):
                fichier_zip.write(fichier, arcname=self.fichiers_archive[i])

        return self

    def send_to_hote(self, ftp):
        self.archive.seek(0)

        if ftp.login(self.configuration.user, self.configuration.password):
            ftp.storbinary("STOR archive.zip", self.archive)
            
            if ftp.size("archive.zip") \
                    == os.fstat(self.archive.fileno()).st_size:
                return True

        return False

    def run(self):
        self.build_liste_fichiers()
        self.build_archive()

        ftp = ftplib.FTP(self.configuration.hote)
        self.send_to_hote(ftp)

if __name__ == '__main__':
    app = SaveFTP()
    app.load_configuration(Configuration())
    app.run()