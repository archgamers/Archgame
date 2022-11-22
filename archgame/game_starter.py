import random

from archgame import game_server
from archgame import constants
from archgame import texts
from archgame import events
from archgame import cli
from archgame import gamers as classes_gamers

FLAG_SLOW_PRINT = False


# Создает экземпляры всех классов
# Запускает главный цикл игры
def game_starter():
    flag_slow_print = False
    q_g = input(texts.ASK_QUANTITY)
    while not q_g.isdigit():
        print("Введите, пожалуйста, цифру, мы такое не понимаем.")
        q_g = input(texts.ASK_QUANTITY)

    q_b = input("Введите количество ботов: ")
    while not q_b.isdigit():
        print("Введите, пожалуйста, цифру, мы такое не понимаем.")
        q_b = input("Введите количество ботов: ")

    q_g = int(q_g)
    q_b = int(q_b)

    gamers = []

    # Создаем ботов
    for i in range(q_b):
        if q_g == 0:
            io_for_all = cli.BotIO(flag_slow_print)
            gamers.append(
                classes_gamers.Bot(i + 1, random.choice(["A", "M", "P"]),
                                   g_cli=io_for_all,
                                   flag_slow_print=FLAG_SLOW_PRINT))
        else:
            gamers.append(
                classes_gamers.Bot(i + 1, random.choice(["A", "M", "P"]),
                                   flag_slow_print=FLAG_SLOW_PRINT))

    # print(texts.ASK_CLASSES)
    for i in range(1, q_g + 1, 1):
        inpt_gamer_name_and_class = ""

        while constants.SEPARATOR not in inpt_gamer_name_and_class:
            inpt_gamer_name_and_class = input(texts.ASK_NAME % i).strip()
        n, cl = inpt_gamer_name_and_class.split(constants.SEPARATOR)

        while cl not in ["M", "М", "A", "А", "P", "Р",
                         "m", "м", "a", "а", "p", "р"]:
            print("Неверно введен класс")
            n, cl = input(texts.ASK_NAME % i).strip().split(
                constants.SEPARATOR)

        if cl in ["M", "М", "m", "м"]:
            cl = "M"
        if cl in ["A", "А", "a", "а"]:
            cl = "A"
        if cl in ["P", "Р", "p", "р"]:
            cl = "P"

        if len(n) > (constants.LIM_LEN_NAME+1):
            n = n[:constants.LIM_LEN_NAME] + "~"

        gamers.append(classes_gamers.Gamer(n.strip(), cl.strip(),
                                           flag_slow_print=FLAG_SLOW_PRINT))
    # print(texts.LEGEND)
    ev = events.Events()
    gserv = game_server.GameServer(gamers, ev)
    gserv.main_cycle()


if __name__ == "__main__":
    game_starter()
