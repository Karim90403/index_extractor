from abc import ABC
from argparse import ArgumentParser, Namespace
from typing import List

from management.base.abc_command import ABCCommand
from management.cmd_parser import Parser


class BaseCommand(ABCCommand, ABC):
    args: Namespace = None
    help: str = None

    def __init__(self, args: List[str], parser: ArgumentParser):
        self.parser = parser
        self.add_arguments()
        self.set_arguments()
        self.args = self.parser.parse_args(args)

    def set_arguments(self):
        self.parser.add_help = self.help
        parser = Parser()
        parser.remove_argument("mode")