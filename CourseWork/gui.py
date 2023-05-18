import PySimpleGUI as sg
import os
from functools import reduce
from layout import layout


class GUI:
    def __init__(self, scanner):
        self.__scanner = scanner
        self.__window = None

    @staticmethod
    def __get_all_lan_ips():
        def ip_to_int(ip):
            return reduce(lambda x, y: x + int(y[1]) * 2 ** (8 * y[0]), enumerate(reversed(ip.split('.'))), 0)

        with os.popen("ifconfig") as fp:
            ifc_data = fp.read().split('\n\n')
        for connection in ifc_data:
            connection_data = connection.split()
            if not len(connection_data):
                continue
            if connection_data[0] == 'lo:':
                continue
            address = connection_data[connection_data.index('inet') + 1]
            netmask = connection_data[connection_data.index('netmask') + 1]
            req = f"{address}/{ip_to_int(netmask).bit_count()}"
            with os.popen(f"nmap -sn {req}") as fp:
                nmap_data = fp.read().split('\n')
            nmap_ip4 = [line.split()[4] for line in nmap_data if line.startswith("Nmap scan")]
            return nmap_ip4

    def run(self):
        print("Проверка существующих IP-адресов в сети...")
        ips = self.__get_all_lan_ips()
        if ips is None:
            print("Нет соединений, возможно только сканирование текущего устройства")
            ips = ["127.0.0.1"]
        self.__window = sg.Window("Сканер портов", layout, finalize=True)
        print("Пользовательский интерфейс загружен")
        self.__window["-COMBO-"].update(values=ips, value=ips[0])
        prev = {"-PORT_START-": 0, "-PORT_END-": 1023}
        results, open_results = list(), list()
        view_all = True
        while True:
            event, values = self.__window.read()
            if event in ("-PORT_START-", "-PORT_END-"):
                try:
                    value = int(values[event])
                    if value > 65535:
                        raise ValueError
                    prev[event] = value
                except ValueError:
                    if values[event]:
                        self.__window[event].update(value=prev[event])
                        continue
            if event == "-SCAN-":
                ips = [values["-COMBO-"]]
                try:
                    ports = [port for port in range(int(values["-PORT_START-"]), int(values["-PORT_END-"]) + 1)]
                except ValueError:
                    self.__window["-RESULTS-"].update("Порты введены некорректно")
                    continue
                chunk, index = 1000, 0
                self.__scanner.total_time = float(0)
                while index < len(ports):
                    self.__scanner.run(ips, ports[index:min(index + chunk, len(ports))])
                    index += chunk
                self.__window["-RESULTS-"].update("")
                results = list(self.__scanner.results)
                self.__scanner.print(gui=self.__window["-RESULTS-"])
                self.__scanner.results = list()
            if event == "-ALL-":
                view_all = True
                if results:
                    self.__window["-RESULTS-"].update("")
                    self.__scanner.results = list(results)
                    self.__scanner.print(gui=self.__window["-RESULTS-"])
                    self.__scanner.results = list()
                else:
                    self.__window["-RESULTS-"].update("Нечего отображать")
            if event == "-OPEN-":
                view_all = False
                open_results = [result for result in results if result[2] == "открыт"]
                if open_results:
                    self.__window["-RESULTS-"].update("")
                    self.__scanner.results = list(open_results)
                    self.__scanner.print(gui=self.__window["-RESULTS-"])
                    self.__scanner.results = list()
                else:
                    self.__window["-RESULTS-"].update("Открытых портов нет")
            if event == "-SORT-":
                if view_all:
                    if results:
                        self.__window["-RESULTS-"].update("")
                        results.sort(key=lambda x: x[1])
                        self.__scanner.results = list(results)
                        self.__scanner.print(gui=self.__window["-RESULTS-"])
                        self.__scanner.results = list()
                    else:
                        self.__window["-RESULTS-"].update("Нечего сортировать")
                else:
                    open_results = [result for result in results if result[2] == "открыт"]
                    if open_results:
                        self.__window["-RESULTS-"].update("")
                        open_results.sort(key=lambda x: x[1])
                        self.__scanner.results = list(open_results)
                        self.__scanner.print(gui=self.__window["-RESULTS-"])
                        self.__scanner.results = list()
                    else:
                        self.__window["-RESULTS-"].update("Нечего сортировать")
            if event in (sg.WIN_CLOSED, "-EXIT-"):
                break
            try:
                if int(values["-PORT_START-"]) > int(values["-PORT_END-"]):
                    if event == "-PORT_START-":
                        self.__window["-PORT_END-"].update(value=prev["-PORT_START-"])
                    else:
                        self.__window["-PORT_START-"].update(value=prev["-PORT_END-"])
            except ValueError:
                pass
        self.__window.close()
