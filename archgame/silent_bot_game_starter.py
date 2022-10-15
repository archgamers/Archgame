import itertools
from archgame import game_server
from archgame import events
from archgame import gamers as classes_gamers
from archgame import cli


# Создает экземпляры всех классов
# Запускает главный цикл игры
def game_starter():
    flag_slow_print = False
    q_game = int(input("Введите количество игр ").strip())
    all_gamers = []
    q_b = input("Введите количество ботов на одну игру ").strip()
    while not q_b.isdigit():
        print("Введите, пожалуйста, цифру, мы такое не понимаем.")
        q_b = input("Введите количество ботов")
    q_b = int(q_b)
    pattern = input("Задайте шаблон классов через запятую")
    for game in range(q_game):
        gamers = []
        io_for_all = cli.EmptyIO(flag_slow_print)
        for i, cl in zip(range(q_b), itertools.cycle(pattern.split(','))):
            gamers.append(classes_gamers.Bot(i + 1, cl, g_cli=io_for_all))
        all_gamers += gamers
        ev = events.Events()
        gserv = game_server.GameServer(gamers, ev)
        gserv.main_cycle()

    # логика сбора статистики с помощью gserv.gamers
    # ключ statistics - Class,
    # значение - [Count,
    # [min_user, sum_user, max_user],
    # [min_cap, sum_cap, max_user]]
    statistics = {"A": [0, [100000, 0, 0], [100000, 0, 0]],
                  "M": [0, [100000, 0, 0], [100000, 0, 0]],
                  "P": [0, [100000, 0, 0], [100000, 0, 0]]}
    for gamer in all_gamers:
        statistics[gamer.class_per][0] += 1

        statistics[gamer.class_per][1][0] = min(
            statistics[gamer.class_per][1][0], gamer.users)
        statistics[gamer.class_per][2][0] = min(
            statistics[gamer.class_per][2][0], gamer.caps)

        statistics[gamer.class_per][1][1] += gamer.users
        statistics[gamer.class_per][2][1] += gamer.caps

        statistics[gamer.class_per][1][2] = max(
            statistics[gamer.class_per][1][2], gamer.users)
        statistics[gamer.class_per][2][2] = max(
            statistics[gamer.class_per][2][2], gamer.caps)

    # записываем вместо суммы среднее значение
    for cl in statistics:
        if statistics[cl][0] != 0:
            statistics[cl][1][1] = round(
                statistics[cl][1][1]/statistics[cl][0], 1)
            statistics[cl][2][1] = round(
                statistics[cl][2][1]/statistics[cl][0], 1)
        else:
            statistics[cl][1] = [0, 0, 0]
            statistics[cl][2] = [0, 0, 0]

    # вызываем эмпти ио, чтобы печатать статистику
    io_for_all.statistic(statistics)


if __name__ == "__main__":
    game_starter()
