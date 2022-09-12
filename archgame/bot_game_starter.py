from archgame import game_server
from archgame import events
from archgame import gamers as classes_gamers
from archgame import cli


# Создает экземпляры всех классов
# Запускает главный цикл игры
def game_starter():
    flag_slow_print = False
    q_b = input("Введите количество ботов ")
    while not q_b.isdigit():
        print("Введите, пожалуйста, цифру, мы такое не понимаем.")
        q_b = input("Введите количество ботов")
    q_b = int(q_b)
    gamers = []
    io_for_all = cli.BotIO(flag_slow_print)
    for i in range(q_b):
        gamers.append(classes_gamers.Bot(i + 1, g_cli=io_for_all))
    ev = events.Events()
    gserv = game_server.GameServer(gamers, ev)
    gserv.main_cycle()


if __name__ == "__main__":
    game_starter()
