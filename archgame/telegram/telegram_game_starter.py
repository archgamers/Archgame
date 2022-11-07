# -*-coding: utf-8 -*-
import telebot
import logging
import uuid
from logging import handlers as log_handlers
from optparse import OptionParser
import game_server
import events
import gamers
import texts
import cli


# Инициализируем логгирование
def log_init(log_file, log_level):
    """
    Function for init log file
    """
    logger = logging.getLogger(__name__)
    # Log Handler. Set logfile
    chandl = log_handlers.WatchedFileHandler(log_file)
    # create formatter for log
    formatter = logging.Formatter(
        '%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
    # add formatter to handler
    chandl.setFormatter(formatter)
    logger.addHandler(chandl)
    # Set log level from config
    logger.setLevel(log_level)


log_init(
    './log.log',
    logging.DEBUG
)
log = logging.getLogger(__name__)

# Парсим входные данные - мы должны сообщить в консоли токен бота
# с помощью -t

parser = OptionParser()

# Available actions
parser.add_option("--log", "-l", dest="logfile", type="string",
                  metavar="LOGFILE", default="/var/log/check_flow.log",
                  help="path to log file. Default is %default")

parser.add_option("--loglevel", dest="loglevel", type="string",
                  metavar="LOGLEVEL", default="DEBUG",
                  help="path to log file. Default is %default")

parser.add_option("--token", "-t", dest="token", type="string",
                  default="None",
                  help="Telegram token. Default is %default")

options, _ = parser.parse_args()

try:
    global bot
    bot = telebot.TeleBot(options.token)
except Exception as err:
    log.exception('aaaaa, this is exception: %s', err)


class GameStorage:
    def __init__(self):
        self.dict_gamers = {}
        self.dict_games = {}

    def add_player(self, user_id, name):
        self.dict_gamers[user_id] = gamers.TelegaGamer(
            name, user_id, g_cli=cli.TelegramIO(bot, user_id))

    def get_gamer(self, user_id):
        return self.dict_gamers[user_id]

    def create_game(self):
        num = uuid.uuid4()
        self.dict_games[num] = []
        return num

    def add_in_game(self, game, player):
        self.dict_games[game] += [player]
        player.game = game

    def start_game(self, num):
        game = game_server.GameServer(self.dict_games[num], events.Events())
        self.dict_games[num] = game
        for gamer in self.dict_games[num]:
            gamer.add_to_game(game)


global all_telega_data
all_telega_data = GameStorage()


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(message, res=False):
    log.info('Start program')
    bot.send_message(message.chat.id, """Здравствуй, дорогой друг!
Как мне тебя величать? Назови свое светлое имя.""")

    bot.register_next_step_handler(message, get_name)


def get_name(message):  # получаем имя и запоминаем его в TelegramServer.users
    name = message.text.strip()
    u_id = message.chat.id
    bot.send_message(message.from_user.id, 'Весьма рад тебе, %s!' % name)
    log.info("Add user " + str(u_id) + " " + name)
    all_telega_data.add_player(u_id, name)
    bot.register_next_step_handler(message, on_user_message)


def on_user_message(message):
    current_id = message.from_user.id
    current_gamer = all_telega_data.get_gamer(current_id)
    status = current_gamer.get_status()

    # Здесь обрабатываются все статусы,
    # напрямую связанные или подводящие к изменениям GameStorage,
    # чтобы никуда его дополнительно не передавать и с собой не таскать
    # В общем, вся начальная развилка выбора варианта игры
    # до её непосредственного начала
    if status == "init":
        text = """Пришло время избрать свой путь:
1. "Хочу попробовать!"
2. Играть с ботами
3. Играть с друзьями"""
        current_gamer.create_keyboard(text, {"choose tryplay": "1",
                                             "choose soloplay": "2",
                                             "choose friendsplay": "3"})
        current_gamer.change_status("answer")
    elif status == "answer":
        pass
    elif status == "tryplay init":
        text = ("Сейчас, дорогой друг, тебе предстоит трудный шаг, будь "
                "внимателен, твой выбор влияет на дальнейшую стратегию игры "
                "- тебе предстоит выбрать класс персонажа") + texts.ASK_CLASSES
        current_gamer.create_keyboard(text, {"admin": "Неустрашимый админ!",
                                             "manager": "Всей душой менеджер",
                                             "proger": "Программист."})
        current_gamer.change_status("answer")
    elif status == "tryplay start":
        pass  # создать игру на него и ботов
    # Пока что не даем выбора подождать, пока придут и напишут в бота другие
    # люди, хотящие играть не с друзьями, но и не с ботами,
    # или играть с ботами, сразу ультиматумом ставим с ботами
    # TODO: в изначальной задумке было не так, но папа сказал: "чё? не успеем."
    #  надо обсудить
    elif status == "soloplay init":
        current_gamer.print_message("Введи количество ботов")
        current_gamer.change_status("soloplay start")
    elif status == "soloplay start":
        try:
            num = int(message.text.strip())
            pass  # создать игру на него и на его кол-во ботов
        except Exception:
            current_gamer.print_message("Введи количество ботов цифрами, "
                                        "пожалуйста.")
    elif status == "friendsplay init":
        text = ("""Чтобы сыграть с друзьями в игру, её нужно сначала создать.
Если кто-то это уже сделал - нажимай Присоединиться.
Если же нет - что ж, не вопрос, давай сделаем это вместе! Жми Создать.""")

        current_gamer.create_keyboard(text, {"add to game": "Присоединиться",
                                             "create game": "Создать"})
        current_gamer.change_status("answer")
    elif status == "create game":
        all_telega_data.add_in_game(all_telega_data.create_game(), current_id)
        text_num = str(all_telega_data.create_game())
        bot.send_message(message.from_user.id, text_num)
        text = """Отлично, игра создана, верховный маг!
Пригласить друзей в неё очень легко - просто пересылай им эти руны.
Когда все пришлют это заклинание, нажми Начать.
Игра начнется у всех одновременно только после твоего веления."""
        current_gamer.create_keyboard(text, {"start game": "Начать"})
        current_gamer.change_status("wait friends")
    elif status == "wait friends":
        pass
    elif status == "add to game":
        current_gamer.print_message("Перешли мне те ужасающие uuid-руны, друг,"
                                    " я с ними разберусь.")
    elif status == "friendsplay start":
        pass  # создать игру на него и друзей
    else:
        # Если это не один из таких статусов, передаем управление Gamer
        current_gamer.fsm(message)
    bot.register_next_step_handler(message, on_user_message)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    current_gamer = all_telega_data.get_gamer(id)
    if call.data == "choose tryplay":
        log.info("User %d chose tryplay" % current_gamer.get_id())
        current_gamer.change_status("tryplay init")

    elif call.data == "admin":
        current_gamer.set_class("A")
        current_gamer.change_status("tryplay start")

    elif call.data == "manager":
        current_gamer.set_class("M")
        current_gamer.change_status("tryplay start")

    elif call.data == "proger":
        current_gamer.set_class("P")
        current_gamer.change_status("tryplay start")

    elif call.data == "choose soloplay":
        log.info("User %d chose soloplay" % current_gamer.get_id())

    # solo_play если ждем
    # solo_play не ждем - выбрать количество ботов, отдать эту инфу в ф-цию

    elif call.data == "choose friendsplay":
        log.info("User %d chose friendsplay" % current_gamer.get_id())
        current_gamer.change_status("wait start friendplay")
        # bot.register_next_step_handler(friends_play)  # пока просто выбор
        # кнопка "выбрать игру / присоединиться к существующей"

    # если пользователь генерит игру - то создать игру
    # и выслать ему код игры "Перешли друзьям, с которыми хочешь сыграть,
    # чтобы они могли к тебе присоединиться"

    # если присоединяется - спросить id и добавить его в игру с этим id
    # для отладки сейчас сделать так, чтобы в dct_games всегда была игра


# Запускаем бота
bot.polling(none_stop=True, interval=0)
