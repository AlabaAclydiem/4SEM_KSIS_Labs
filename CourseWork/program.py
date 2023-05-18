from parser import Parser
from scanner import Scanner
from gui import GUI


class Program:
    def __init__(self):
        self.__parser = Parser()
        self.__scanner = Scanner()
        self.__gui = GUI(self.__scanner)

    def run(self):
        if self.__parser.arguments["gui"]:
            self.__gui.run()
        else:
            ips = [self.__parser.arguments["ip"]]
            ports = [port for port in range(self.__parser.arguments["port"], self.__parser.arguments["port_end"] + 1)]
            chunk, index = 1000, 0
            while index < len(ports):
                self.__scanner.run(ips, ports[index:min(index + chunk, len(ports))])
                index += chunk
            self.__scanner.print()
