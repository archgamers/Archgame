# -*-coding: utf-8 -*-
from archgame import constants

ASK_QUANTITY = "Сколько будет игроков? "
ASK_CLASSES = """\
Классы игроков:
М - Менеджер, невероятно обаятелен, каждый ход к нему просто так приходит 1
    krps
Р - Программист, властелин-АПИ, у него они держат больше остальных - целых 5
    krps каждая
А - Админ, неустрашим - в его кармане всегда есть флешка с продом, backup
    встроенный, не падает DB ни при каких обстоятельствах"""
ASK_NAME = "Введите имя и класс игрока(через запятую) %d "

CLASSES_USER_READABLE = {
    constants.MANAGER_CLASS: 'Менеджер',
    constants.PROGRAMMER_CLASS: 'Программист',
    constants.ADMIN_CLASS: 'Админ',
}

LEGEND = """\
A - API: умеет принимать нагрузку от пользователей, может выдержать до {0}krps
    нагрузки, для работы нужна DB

D - DB: умеет обрабатывать запросы от API, может поддерживать до {1}х API

L - LoadBalancer: Позволяет масштабировать API, без него максимальная
    производительность всех API не превышает производительности одного API.
    Может обслуживать не больше {2}х API

B - Backup: В случае ошибки DBA позволяет избежать потери пользовательской
    базы, но снимается с игрового поля.
""".format(constants.LIM_A, constants.LIM_D, constants.LIM_L)

SPRINTS = "Спринт %d:"

INPUT_ACTION = "Введите действие для игрока %s: "

DESC = """
Вам пришло финансирование, у каждого игрока есть %i очка, которые он может
потратить либо на привлечение новых пользователей(1), либо на установку новых
сервисов(2):
"""

ENDING = "Поздравляем победителя %s!!!"

INVALID_USER_INPUT = ('Некорректный ввод, пожалуйста, попробуйте снова, '
                      'помните, что на ход вам даётся %d очка')

EVENT_FAILED = ("Событие сломалось, для этого игрока ничего не происходит"
                ", играем дальше.")

# Texts for telegram mode

# Пришлось написать длинные строки в одну линию, т к у Telegram свое
# представление о форматировании и длине строки
TELEGRAM_HELP = """Доступные команды:
/start Вывести это сообщение.
/help Вывести это сообщение.
/trial [<Имя>] [<Класс>=(A|M|P)] Попробовать игру.
    Игра начнется для игрока, которого зовут <Имя> и его класс в игре будет <Класс>. Если <Имя> или <Клаcc> не указаны при вызове команды, то будет выбрано значение по умолчанию.  Вместе с ним в игру будут играть два бота, которые будут названы Bot0 и Bot1. Они будут представлять оставшиеся классы.
/new [<Имя>] [<Класс>=(A|M|P)] Создать новую игру.
    Игра будет ждать начала через команду /run. После выполнения этой команды будет сгенерирован код, который надо переслать другим игрокам. Имя в этой игре у данного игрока будет <Имя>, а класс соответственно <Класс>. Если <Имя> или <Клаcc> не указаны, то будут выбраны значения по умолчанию.
/run Запустить ранее созданную игру.
    Команда будет выполнена только если игра была создана перед этим командой /new
/join [<Имя>] [<Класс>=(A|M|P)] Подключиться к созданной игре.
    Подключиться к созданной игре с именем <Имя> и классом <Класс>. После выполнения команды будут запрошен код игры, который можно получить от того, кто создавал игру командой /new.
/reset Завершить текущую игру.
    В случае игры с другими людьми она будет завершена, если вы являлись создателем
/status Посмотреть текущее состояние.
    Покажет какое текущее состояние для данного игрока.
/rules Посмотреть правила игры.
"""  # noqa: E501
TELEGRAM_GAME_ALREADY_STARTED = ("Игра для вас уже начата. Если вы хотите "
                                 "начать новую игру, то нужно предварительно "
                                 "завершить текущую через команду /reset")
TELEGRAM_GAME_NOT_STARTED = ("Нету ни одной ожидающей старта игры. Создайте"
                             "новую игру через команду /new, чтобы"
                             "воспользоваться этой командой")
TELEGRAM_START_FORBIDEN = ("Нельзя запустить чужую игру. Это должен сделать "
                           "создатель игры.")
TELEGRAM_USER_INFO = 'Вы участвуете в игре под именем "%s" и c классом %s'
TELEGRAM_JOIN_INFO = ("Вы начали процесс подключения к игре. Следующим шагом "
                      "нужно ввести правильный идентификатор игры. Попросите "
                      "создателя игры переслать его вам, после этого "
                      "перешлите его боту. Остановить процесс подключения "
                      "можно командой /reset")
TELEGRAM_JOIN_GAME_FAIL = "Игра с индентификатором %s не найдена."
TELEGRAM_JOIN_GAME_RESET = "Вы остановили процесс подключения к игре."

TELEGRAM_GAME_STARTED_STATUS = "Вы сейчас играете в игру %s"
TELEGRAM_GAME_CREATED = ("Игра создана. Перешлите ее номер другим игрокам. "
                         "После того как они вступят в нее через команду "
                         "/join вы сможете начать с помощью команды /run. "
                         "Через команду /status можно контролировать сколько "
                         "человек присоединилось.")
TELEGRAM_GAME_IDLE_STATUS = "Вы сейчас не играете ни в одну игру"
TELEGRAM_GAME_RESET_SUCCESS = "Игра %s завершена."
TELEGRAM_GAME_NOT_OWNER = ("Вы не можете сбросить игру %s, поскольку не "
                           "являтесь ее владельцем")
TELEGRAM_STATUS_PLAYERS_INTRO = "Вместе с вами играют:"
TELEGRAM_STATUS_PLAYER_INFO = "Игрок %s с классом %s находится в статусе: %s"
TELEGRAM_USER_STATUS_HUMAN_READABLE = {
    constants.USER_INIT_ST: "Ожидает начала игры",
    constants.USER_WAIT_ST: "Вводит данные",
    constants.USER_READY_ST: "Ждет пока сходят остальные",
    constants.USER_JOIN_ST: "Подключается к игре",
}
# Пришлось написать длинные строки в одну линию, т к у Telegram свое
# представление о форматировании и длине строки
TELEGRAM_RULES = """Описание игры:
Вам выдали небольшое количество серверов, несколько стоек. Ваша задача - построить систему, которая выдерживает максимально возможную нагрузку пользователей. Большую, чем у ваших конкурентов. На это у вас есть несколько спринтов. Нагрузка от пользователей измеряется в krps(тысячах запросов в секунду). Цель игры - научить основам проектирования архитектуры и отказоустойчивости при построении реальных систем.

Игровое поле:
Игровое поле предствляет собой доступные вам ресурсы. Это квадратная доска 4х4 клеточки. Каждая клеточка обозначает один сервер, на котором можно разместить любой сервис, но только один. Колонки представляют собой стойки(группы серверов с общим питанием и сетью). Нумерация ячеек сквозная - в левом верхнем углу сервер номер 1, в правом нижнем - номер 16. Не забывайте - сервера или стойки могут выходить из строя! Подходите вдумчиво к расположению ваших сервисов на игровом поле.

Составные части системы:
Вашу систему вы сможете строить из нескольких типов сервисов:
A - API: умеет принимать нагрузку от пользователей, может выдержать до 3rps нагрузки, для работы нужна DB
D - DB: умеет обрабатывать запросы от API, может поддерживать до 3х API
L - LoadBalancer: Позволяет масштабировать API, без него максимальная производительность всех API не превышает производительности одного API. Может обслуживать нe больше 3х API
B - Backup: В случае ошибки DBA позволяет избежать потери пользовательской базы, но снимается с игрового поля.
По итоговому расположению можно посчитать максимальную нагрузку от пользователей, которую может выдержать ваша система(capacity). Например: для системы из 3х API, одного LB и одной DB это будет 9k. Вся лишняя нагрузка, например от событий, будет сбрасываться до текущей capacity. Если вы хотите, чтобы ваша система выдерживала большую нагрузку - добавляйте сервисов.

Каждый спринт состоит из нескольких стадий:
1. Принятие решений. Вам выдают некоторое кол-во ресурсов(несколько очков). Вы можете потратить их либо на расширение системы, либо на привлечение клиентов.  Расширение системы происходит через добавление компонентов. Один компонент стоит одно очко. В первый спринт вам доступно 4 очка, в последующие - по 2 очка. Формат ввода для этого шага смотри ниже.
2. Срабатывание событий. Они могут быть как положительные, так и отрицательные. Могут влиять и на вашу систему и на нагрузку от пользователей.
3. Актуализация состояния вашего сериса.

Определение победителя:
По завершению финального спринта(7) происходит сравнение текущего кол-ва нагрузки и выбирается один или несколько победителей.

Классы игроков:
Можно выбрать один из классов игроков в начале игры. Каждый обладает своими преимуществами:
М - Менеджер, невероятно обаятелен, каждый ход к нему просто так приходит 1 krps.
Р - Программист, властелин-API, у него они держат больше остальных - целых 5 krps каждая.
А - Админ, неустрашим - в его кармане всегда есть флешка с продом, backup встроенный, не падает DB ни при каких обстоятельствах.

Формат ввода для шага принятия решений:
Во время принятия решения у вас есть несколько очков, которые вы можете потратить. Каждое из них можно потратить либо на привлечение пользователя - введя 1, либо на установку сервиса - введя 2-Название_сервиса-номер_сервера.  Ввод решений нужно разделять запятыми. Примеры: 1,2-A-1 - потратить одно очко на привлечение новых пользователей, а на второе очко запустить API в сервере номер 1(левая верхняя ячейка доски, про нумерацию смотри раздел Игровое поле).
"""  # noqa: E501
