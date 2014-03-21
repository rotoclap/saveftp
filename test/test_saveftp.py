#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

import ftplib
import unittest
from unittest.mock import Mock, PropertyMock
import os
import zipfile

from saveftp import SaveFTP

class TestSaveFTP(unittest.TestCase):
    def setUp(self):
        """Initialisation du test.

        Creation d'un mock de configuration
        Creation de l'instance de l'application
        """

        self.base_chemin = os.path.dirname(os.path.abspath(__file__)) \
            + "\\test_path_archive"
        self.base_repertoire = os.path.basename(self.base_chemin)

        self.configuration = Mock()
        self.configuration.user = "anonymous"
        self.configuration.password = None
        self.configuration.hote = "localhost"
        self.configuration.source = self.base_chemin

        self.app = SaveFTP()

        

        self.reference_fichiers = [
            self.base_chemin + "\\file1.txt",
            self.base_chemin + "\\file2.txt",
            self.base_chemin + "\\file3.txt",
            self.base_chemin + "\\subdirectory\\file4.txt",
        ]

        self.reference_fichiers_archive = [
            self.base_repertoire + "\\file1.txt",
            self.base_repertoire + "\\file2.txt",
            self.base_repertoire + "\\file3.txt",
            self.base_repertoire + "\\subdirectory\\file4.txt",
        ]


    def tearDown(self):
        SaveFTP._instance = None

    def test_load_configuration(self):
        """Test de chargement du fichier de configuration.

        Le test reussi si l'instance enregistree dans l'application
        est du meme type que l'instance passee a la methode.
        """
        self.app.load_configuration(self.configuration)
        self.assertIsInstance(self.app.configuration, 
            type(self.configuration))

    def test_build_liste_fichiers(self):
        """Test de la liste des fichiers à archiver."""
        
        self.configuration.source = self.base_chemin
        self.app.load_configuration(self.configuration)

        self.app.build_liste_fichiers()

        self.assertListEqual(self.app.fichiers, self.reference_fichiers)
        self.assertListEqual(self.app.fichiers_archive, 
            self.reference_fichiers_archive)
        
    def test_build_archive(self):
        """Test de l'archivage des fichiers.

        Le test reussi si la liste des fichiers extraits de l'archive
        venant d'être creee correspondant a la liste des fichiers
        devant etre archives.
        """

        self.configuration.source = self.base_chemin
        self.app.load_configuration(self.configuration)
        
        self.app.fichiers = self.reference_fichiers
        self.app.fichiers_archive = self.reference_fichiers_archive
        self.app.build_archive()

        with zipfile.ZipFile(self.app.archive, mode="r") as zip_file:
            zip_fichiers = \
                [fichier.replace("/", "\\") for fichier in zip_file.namelist()]

            self.assertListEqual(zip_fichiers, self.reference_fichiers_archive)

        self.assertGreater(os.fstat(self.app.archive.fileno()).st_size, 0)

    def test_send_to_hote(self):
        """Test de l'envoi FTP.

        La fonction renvoie True si tout s'est bien passé.
        """

        self.app.load_configuration(self.configuration)
        self.app.fichiers = self.reference_fichiers
        self.app.fichiers_archive = self.reference_fichiers_archive
        self.app.build_archive()

        zip_file = zipfile.ZipFile(self.app.archive, mode="r")

        ftp = ftplib.FTP(self.app.configuration.hote)
        self.assertTrue(self.app.send_to_hote(ftp))
        ftp.close()
