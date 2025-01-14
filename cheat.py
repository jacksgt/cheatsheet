#!/usr/bin/python3
"""
Ok this whole thing is pretty straight forward I guess.

To add a new output format:

Add the new command-line option to the printer group, like so:
    group.add_argument('-x', help=help_MyNewPrinter, action='store_const', dest='printer', const='MyNewPrinter')

And then create a new Printer Subclass based on the name you just added. It should the implement the printCheatSheet method:
    class MyNewPrinter(Printer)
"""

from configparser import ConfigParser
from argparse import ArgumentParser
from sys import path
from sys import exit

#TODO: Maybe get rid of the duplicate for loops somehow.
class Printer:

    def __init__(self, configparser):
        self.configparser = configparser

    def printsheet(self):
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

    def printsheet(self):
        for description in self.configparser['cheats']:
            value = self.configparser['cheats'][description]
            output = "{0:<{1}} {2}".format(description, self.width, value)

            print(output)

class BreaklinePrinter(Printer):
    """
    Prints the cheatsheet with newlines
    """

    def printsheet(self):
        for description in self.configparser['cheats']:
            value = self.configparser['cheats'][description]
            output = "{0} \n {1}".format(description, value)

            print(output)

def main():
    #GENERAL SETTINGS!
    directory      = path[0] + "/config/"
    extention      = ".ini"
    description    = "Cool Command-line Cheatsheets"
    help_general   = "The cheatsheet you want to see"
    help_inline    = "One cheat per line, this is default"
    help_breakline = "Break lines"

    #COMMAND-LINE ARGUMENTS!
    argumentparser = ArgumentParser(description=description)
    printertype = argumentparser.add_mutually_exclusive_group()

    argumentparser.add_argument('cheatsheet', help=help_general)
    printertype.set_defaults(printer='InlinePrinter')
    printertype.add_argument('-l', help=help_inline, action='store_const', dest='printer', const='InlinePrinter')
    printertype.add_argument('-b', help=help_breakline, action='store_const', dest='printer', const='BreaklinePrinter')

    #WHERE THE RUBBER MEETS THE ROAD!
    cmd_arguments = argumentparser.parse_args()
    filename = directory + cmd_arguments.cheatsheet + extention
    CheatPrinterConstructor = globals()[cmd_arguments.printer]
    configparser = ConfigParser()
    cheatprinter = CheatPrinterConstructor(configparser)

    try:
        configparser.read(filename)
        cheatprinter.printsheet()
        exitcode = 0
    except:
        #I know lazy handling, but it works perfect... Sorry.
        print(filename + " not available or contains errors.")
        exitcode = 1
    finally:
        exit(exitcode)

if __name__ == "__main__":
    main()
