import os
from functools import partial
from collections import defaultdict
from pathlib import Path
from string import Template

__author__ = "Garry Galler"
__version__ = "1.0.1"
# -------------------------------------
ROOT = os.path.abspath('.').lower()
LAST_SCANDIR = defaultdict(list)
COLOR = {}
RESET = ''
# -------------------------------------
try:
    import colorama
except ImportError:
    pass
else:
    colorama.init(autoreset=True)
    from colorama import Fore, Back, Style

    RESET = Style.RESET_ALL
    COLOR.update({
        'file': Fore.GREEN,
        'dir': Fore.BLUE,
        'link': Fore.MAGENTA,
        'back': Back.CYAN,
        'bright': Style.BRIGHT,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'yellow': Fore.YELLOW,
        'red': Fore.RED,
    })

PROMPT_TEMPLATE = Template('''
$back$exit      $reset$red Выход $reset
$back$clear      $reset$yellow Очистка экрана $reset
$back$current   $reset$cyan$bright $root $reset'''
                           )

PROMPT_KWARGS = dict(
    root=ROOT,
    exit=':exit, :e',
    clear=':clear,:c',
    current='current_path',
    reset=RESET,
    back=COLOR.get('back', ''),
    red=COLOR.get('red', ''),
    yellow=COLOR.get('yellow', ''),
    cyan=COLOR.get('cyan', ''),
    bright=COLOR.get('bright', '')
)


def clear():
    '''очистка экрана консоли'''
    os.system('cls' if os.name == 'nt' else "clear")
    return None, None


def type_entry(entry):
    '''определяем тип записи'''
    types = {
        entry.is_dir(): 'dir',
        entry.is_file(): 'file',
        entry.is_symlink(): 'link'
    }

    return types.get(True)


def get_path_from_int(inp):
    '''получает имя записи по номеру, если передано число;
    если номер отсутствует, то число возвращается как есть,
    интерпретируясь как имя директории или файла;
    если передано не число, возвращаем как есть
    '''
    if ROOT in LAST_SCANDIR:
        try:
            inp = LAST_SCANDIR[ROOT][int(inp)]
        except (ValueError, IndexError):
            pass
        else:
            inp = inp.name
    return inp


def get_path_from_link(path):
    '''получает реальный путь из символической ссылки'''
    result = []
    path = path

    def inner():
        nonlocal result, path
        if Path(path).is_symlink():
            path = os.readlink(path)
            result.append(path)
            return inner()
        return result

    return inner


def enum_dir(inp):
    '''перечисление содержимого директории в виде записей
    класса DirEntry
    '''
    global ROOT
    add_entries = True
    path = inp

    if ROOT != inp:
        link = get_path_from_link(inp)()
        # для отображения в консоли добавляем все пути
        path += '' if not link else ' -> ' + ' -> '.join(link)
        ROOT = inp  # оставляем путь как есть, так как ОС сама разрулит переход по ссылке

    print('ROOT:', path)

    if ROOT in LAST_SCANDIR:
        entries = LAST_SCANDIR[ROOT]
        add_entries = False
    else:
        entries = os.scandir(inp)

    for i, entry in enumerate(entries):
        link = ''
        te = type_entry(entry)
        link = get_path_from_link(entry.path)()
        links = '' if not link else ' -> ' + ' -> '.join(link)
        name = entry.name

        if entry.is_dir():
            name += "/"

        name = ''.join([COLOR.get(te, ''), name, RESET])

        if entry.is_file():
            name += ":"
            name = ''.join(
                [name,
                 COLOR.get('cyan', ''),
                 str(round(entry.stat().st_size / 1024, 3)),
                 ' kb',
                 RESET
                 ]
            )

        print("{:4}:{}:{}{}".format(i, name, te, links))

        if add_entries:
            LAST_SCANDIR[ROOT].append(entry)


def after_input(inp):
    '''если передан файл - возвращаем его;
    если директория - перечисляем ее содержимое'''

    result = None, None
    inp = get_path_from_int(inp)

    if not os.path.isabs(inp):
        inp = os.path.realpath(os.path.join(ROOT, inp))

    if os.path.exists(inp):
        if Path(inp).is_file():
            link = get_path_from_link(inp)()
            result = 1, inp if not link else link[-1]
        else:
            enum_dir(inp)
    # not exists
    else:
        result = 0, inp
    return result


def get_selected_file():
    '''цикл опроса и возврата выбранного файла'''
    result = None, None
    while 1:

        PROMPT_KWARGS.update({'root': ROOT})
        PROMPT = PROMPT_TEMPLATE.substitute(**PROMPT_KWARGS)
        print(PROMPT)

        inp = input('#>>:')

        # если вам скажут, что в Python нет switch - покажите ему это:
        result = {
            '': partial(after_input, ROOT.lower()),
            ':exit': lambda: (-1, None),  # выход из цикла, без выхода из приложения
            ':clear': clear,  # очистка экрана консоли
            ':e': lambda: (-1, None),
            ':c': clear
        }.get(inp,
              # ветка default
              partial(after_input, inp.lower())
              )()

        if result[0] == 0:
            print("Path not found:", result[1])
        # выходим, если получили что-то отличное от None
        elif result[0] is not None:
            break

    return result


if __name__ == "__main__":
    err, sfile = get_selected_file()
    if err != -1:
        print("Выбран файл:", COLOR['back'] + sfile + RESET)
    else:
        print("Файл не выбран")