#!/usr/bin/python3
"""
Ok this whole thing is pretty straight forward I guess.

To add a new output format:

Add the new command-line option to the printer group, like so:
    group.add_argument('-x', help=help_MyNewPrinter, action='store_const', dest='printer', const='MyNewPrinter')

And then create a new Printer Subclass based on the name you just added. It should the implement the printCheatSheet method:
    class MyNewPrinter(Printer)
"""

import configparser
import argparse
from sys import path
from sys import exit

class Printer:

    def __init__(self, configparser):
        self.configparser = configparser

    def printCheatSheet(self):
        raise NotImplementedError

class InlinePrinter(Printer):
    """
    Prints the cheatssheet inline, so that it's grep-able.
    """

    @property
    def width(self):
        width = 10

        for description in self.configparser['cheats']:
            if len(description) > width:
                width = len(description)

        return width

    def printCheatSheet(self):
        for description in self.configparser['cheats']:
            value = self.configparser['cheats'][description]
            output = "{0:<{1}} {2}".format(description, self.width, value)

            print(output)

class BreaklinePrinter(Printer):
    """
    Prints the cheatsheet with newlines
    """

    def printCheatSheet(self):
        for description in self.configparser['cheats']:
            value = self.configparser['cheats'][description]
            output = "{0} \n {1}".format(description, value)

            print(output)

def main():
    #GENERAL SETTINGS
    directory = path[0] + "/config/"
    extention = ".ini"
    description = "Cool Command-line Cheatsheets"
    help_general = "The cheatsheet you want to see"
    help_inline = "One cheat per line, this is default"
    help_breakline = "Break lines"
    parser = configparser.ConfigParser()

    #COMMAND-LINE ARGUMENTS!
    argumentParser = argparse.ArgumentParser(description=description)
    argumentParser.add_argument('cheatsheet', help=help_general)
    group = argumentParser.add_mutually_exclusive_group()
    group.set_defaults(printer='InlinePrinter')
    group.add_argument('-l', help=help_inline, action='store_const', dest='printer', const='InlinePrinter')
    group.add_argument('-b', help=help_breakline, action='store_const', dest='printer', const='BreaklinePrinter')
    cmd_arguments = argumentParser.parse_args()

    #WHERE THE RUBBER MEETS THE ROAD!
    CheatPrinterConstructor = globals()[cmd_arguments.printer]
    filename = directory + cmd_arguments.cheatsheet + extention

    try:
        parser.read(filename)
        cheatPrinter = CheatPrinterConstructor(parser)
        cheatPrinter.printCheatSheet()
    except configparser.Error as exception:
        print(exception)
    except:
        #I know the Printer class should handle this... but I was lazy. Sorry.
        print(filename + " not available or contains errors.")

    exit(0)

if __name__ == "__main__":
    main()
