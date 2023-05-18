import asyncio
import socket
from time import perf_counter, ctime, time
from contextlib import contextmanager


class Scanner:
    def __init__(self):
        self.__timeout = 10.0
        self.__loop = asyncio.get_event_loop()
        self.total_time = float(0)
        self.results = list()
        self.ports = list()
        self.ips = list()

    @contextmanager
    def __timer(self):
        start_time = perf_counter()
        yield
        self.total_time += perf_counter() - start_time

    @property
    def __scan_tasks(self):
        return [self.__scan(ip, port) for port in self.ports for ip in self.ips]

    async def __scan(self, ip, port):
        try:
            await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=self.__timeout)
            state, message = "открыт", "SYN/ACK"
        except (ConnectionRefusedError, asyncio.TimeoutError, OSError) as error:
            messages = {
                "ConnectionRefusedError": "Соединение запрещено",
                "TimeoutError": "Нет ответа",
                "OSError": "Ошибка сети",
            }
            state, message = "закрыт", messages[error.__class__.__name__]
        try:
            service = socket.getservbyport(port)
        except OSError:
            service = 'неизвестно'
        self.results.append((ip, port, state, service, message))

    def run(self, ips, ports):
        self.ips = ips
        self.ports = ports
        with self.__timer():
            self.__loop.run_until_complete(asyncio.wait(self.__scan_tasks))

    def print(self, *, gui=None):
        def expand(text, size=18):
            string = str(text) + " " * max(0, size - len(str(text)))
            return string

        ips = " | ".join(self.ips)
        ports_num = len(self.results)
        if gui is None:
            self.results.sort(key=lambda x: x[1])
            output = '    {: ^12}{: ^8}{: ^12}{: ^20}{: ^12}'
            print(f'Начало асинхронного сканирования портов в момент времени\n{ctime(time())}')
            print(f'Отчёт о сканировании адреса {ips}')
            print(output.format('IP-адрес', 'Порт', 'Состояние', 'Служба', 'Сообщение'))
            for result in self.results:
                print(output.format(*result))
            print(f"\nСканирование {ports_num} портов завершено за {self.total_time:.2f} секунд")
        else:
            output = '{}{}{}{}{}'
            gui.update(f'Отчёт о сканировании адреса\n{ips}\n\n', append=True)
            gui.update(output.format(expand('IP-адрес'), expand('Порт'), expand('Состояние'),
                                     expand('Служба'), expand('Сообщение')) + '\n', append=True)
            for result in self.results:
                gui.update(output.format(expand(result[0]), expand(result[1]), expand(result[2]),
                                         expand(result[3]), expand(result[4])) + '\n', append=True)
            gui.update(f"\nОтображено {ports_num} портов. "
                       f"Полное сканирование было завершено за {self.total_time:.2f} секунд",
                       append=True)
