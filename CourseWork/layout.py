import PySimpleGUI as sg

layout_input_column = [
    [sg.Text('Выберите IP-адрес из доступных:', font="Lucida", size=(30, 1), justification="left")],
    [sg.Combo([], size=(25, 1), key="-COMBO-", font='Lucida', readonly=True)],
    [sg.Text('Введите начальный порт сканирования:', font="Lucida", size=(40, 1), justification="left")],
    [sg.InputText(size=(25, 1), enable_events=True, font="Lucida", key="-PORT_START-", default_text=0)],
    [sg.Text('Введите конечный порт сканирования:', font="Lucida", size=(40, 1), justification="left")],
    [sg.InputText(size=(25, 1), enable_events=True, font="Lucida", key="-PORT_END-", default_text=1023)],
    [sg.HSeparator()],
    [
        sg.Button("Начать сканирование", key="-SCAN-", font="Lucida", size=(15, 2)),
        sg.Button("Выйти из программы", key="-EXIT-", font="Lucida", size=(15, 2))
    ],
]

layout_result_column = [
    [sg.Text('Результаты сканирования:', font="Lucida", size=(30, 1), justification="left")],
    [sg.Multiline(size=(120, 16), disabled=True, key="-RESULTS-", font=("Liberation Mono", 12))],
    [
        sg.Button("Отсортировать результаты", key="-SORT-", font="Lucida", size=(25, 1)),
        sg.Button("Отобразить открытые порты", key="-OPEN-", font="Lucida", size=(25, 1)),
        sg.Button("Отобразить все порты", key="-ALL-", font="Lucida", size=(25, 1)),
    ],
]

layout = [
    [
        sg.Column(layout_input_column),
        sg.VSeparator(),
        sg.Column(layout_result_column),
    ],
]
