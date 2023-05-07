import argparse as ap


class Parser:
    def __init__(self):
        self.__parser = self.__init_parser()

        self.arguments = self.__parser.parse_args()

    @staticmethod
    def __init_parser():
        parser = ap.ArgumentParser(description="Программа, сканирующая заданный диапазон "
                                                                            "портов на заданном диапазоне адресов",
                                          add_help=False)
        parser.add_argument("-h", "--help", help="Открыть справку о программе и выйти. Используется без указания "
                                                        "позиционных аргументов", action="help")
        parser.add_argument("-g", "--gui", help="Открыть программу в графическом режиме. Используется без "
                                                       "указания позиционных параметров", action="store_true")
        parser.add_argument("-i", "--ip", help="Начальный IP-адрес", metavar="I", nargs='?', default=None)
        parser.add_argument("-ie", "--ip_end", help="Конечный IP-адрес", metavar="IE", default=None)
        parser.add_argument("-p", "--port", help="Начальный порт", type=int, metavar="P", nargs='?', default=None)
        parser.add_argument("-pe", "--port_end", help="Конечный порт", type=int, metavar="PE", default=None)

        return parser
