#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

import unittest
from unittest.mock import Mock, PropertyMock

from configuration import Configuration

class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.parser = Mock()
        self.parser.is_valide.return_value = True

        self.configuration = Configuration()

    def test_password_ignored_if_user_anonymous(self):
        self.parser.get_parametres.return_value = {
            "source": "some_path",
            "hote": "remote_server",
            "port": 42,
            "user": "anonymous",
            "password": "password"
        }

        self.configuration.load_from_command_line(self.parser)

        self.assertEqual("some_path", self.configuration.source)
        self.assertEqual("remote_server", self.configuration.hote)
        self.assertEqual(42, self.configuration.port)
        self.assertEqual("anonymous", self.configuration.user)
        self.assertEqual(None, self.configuration.password)

