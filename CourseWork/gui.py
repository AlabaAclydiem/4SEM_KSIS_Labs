from scanner import Scanner


class GUI:
    def __init__(self, scanner):
        self.__scanner = scanner

    def run(self):
        print(self.__scanner.arguments)
        print("GUI is under working...")
