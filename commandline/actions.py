#!/usr/bin/python3.3
# -*-coding:Utf-8 *-

import argparse

class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values in range(1, 65536):
            setattr(namespace, self.dest, values)
        else:
            parser.error("argument port: invalid choice '{}' (choose a value \
between 1 and 65535)".format(values))
