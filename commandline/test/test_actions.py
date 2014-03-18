#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

import unittest
from unittest.mock import Mock, PropertyMock
from argparse import ArgumentError

from commandline.actions import PortAction

class TestPortAction(unittest.TestCase):
    def setUp(self):
        self.parser = Mock()
        self.parser.error = PropertyMock(side_effect=ArgumentError(None, ""))
        
        self.namespace = unittest.mock.MagicMock()
        self.namespace.port = None

        self.action = PortAction(option_strings="", dest="port")

    def test_port_in_range(self):
        self.action.__call__(self.parser, self.namespace, 21)

        self.assertEqual(21, self.namespace.port)

    def test_port_out_of_range(self):
        self.assertRaises(
            ArgumentError, 
            self.action.__call__, 
            parser=self.parser, 
            namespace=self.namespace, 
            values=100000
        )
