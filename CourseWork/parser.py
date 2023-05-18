import argparse


class Parser:
    def __init__(self):
        self.__parser = self.__init_parser()
        self.arguments = self.__get_arguments(self.__parser.parse_args())

    @staticmethod
    def __init_parser():
        parser = argparse.ArgumentParser(description="Программа, сканирующая заданный диапазон "
                                                     "портов на заданном адресе",
                                          add_help=False)
        parser.add_argument("-h", "--help", help="Открыть справку о программе и выйти. Используется без указания "
                                                 "позиционных аргументов", action="help")
        parser.add_argument("-g", "--gui", help="Открыть программу в графическом режиме. Используется без "
                                                "указания позиционных параметров", action="store_true")
        parser.add_argument("-i", "--ip", help="Начальный IP-адрес", metavar="I", default=None)
        parser.add_argument("-p", "--port", help="Начальный порт", type=int, metavar="P", default=None)
        parser.add_argument("-pe", "--port_end", help="Конечный порт", type=int, metavar="PE", default=None)

        return parser

    @staticmethod
    def __get_arguments(ap_namespace_args):
        arguments = dict(vars(ap_namespace_args))
        if arguments["port"] is None:
            arguments["port"] = 0
        else:
            arguments["port"] = min(arguments["port"], 65535)
            arguments["port"] = max(arguments["port"], 0)
        if arguments["port_end"] is None:
            arguments["port_end"] = 1023
        else:
            arguments["port_end"] = min(arguments["port_end"], 65535)
            arguments["port_end"] = max(arguments["port_end"], 0)
        if arguments["ip"] is None:
            arguments["ip"] = "127.0.0.1"
        if arguments["port_end"] < arguments["port"]:
            arguments["port_end"], arguments["port"] = arguments["port"], arguments["port_end"]
        return arguments
