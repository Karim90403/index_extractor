import sys

from management.cmd_parser import Parser

if __name__ == "__main__":
    parser = Parser()
    parser.parse_commands(sys.argv[1:])

