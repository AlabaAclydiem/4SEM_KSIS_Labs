from parser import Parser
from scanner import Scanner
from gui import GUI


class Program:
    def __init__(self):
        self.__parser = Parser()
        self.__scanner = Scanner(self.__parser.arguments)
        self.__gui = GUI(self.__scanner)

    def run(self):
        if self.__parser.arguments.gui:
            self.__gui.run()
        else:
            self.__scanner.run()
