# -*-coding: utf-8 -*-
from archgame import texts
from archgame import constants


class GameServer:
    def __init__(self, gamers, events):
        self.gamers = gamers
        self.events = events

    def print_all(self, text):
        print_for_cli = False
        for gamer in self.gamers:
            if gamer.is_cli:
                if not print_for_cli:
                    gamer.print_message(text)
                    print_for_cli = True
                else:
                    pass
            else:
                gamer.print_message(text)

    def events_run(self):
        for num in range(len(self.gamers)):
            try:
                self.events.random_event(self.gamers, num)
            except Exception:
                self.gamers[num].print_message(
                     "Событие сломалось, для этого игрока ничего не происходит"
                     ", играем дальше.")
            self.gamers[num].class_benefit()

    def begin(self, num_sprint):
        # self.print_all('\n\n\n')
        self.print_all(texts.SPRINTS % num_sprint)
        if num_sprint == 1:
            self.print_all(texts.DESC % constants.FIRST_SPRINT_POINTS)
        else:
            self.print_all(texts.DESC % constants.LIM_POINTS)

    def print_boards(self):
        all_boards = []
        for gamer in self.gamers:
            all_boards.append(gamer.print_board())

        for first_line_all_boards in zip(*all_boards):
            self.print_all("".join(first_line_all_boards).strip())

    def final(self, winner):
        self.print_all(texts.ENDING % winner)

    def main_cycle(self):
        winner = None
        num_sprint = 1
        while winner is None:
            self.begin(num_sprint)
            self.print_boards()
            for gamer in self.gamers:
                gamer.action()
                # Возвращаем всем дефолтные очки на ход
                # Так как BankruptEvent устанавливает лимит
                # на следующий спринт,
                # это нужно делать здесь.
                gamer.default_points()
            self.print_boards()
            # разыграть рандомные события
            self.events_run()

            # Наводим порядок
            # Проверка после эвента: тянет ли своих пользователей
            # после действий ВСЕХ теперь его конструкция
            for gamer in self.gamers:
                gamer.check_user()

            # Условие победы пока не определено, поставила первое попавшееся
            if num_sprint == constants.WIN_SCORE:
                max_users = -1
                winner = []
                for gamer in self.gamers:
                    if gamer.users > max_users:
                        max_users = gamer.users
                        winner = [gamer.name + " " + gamer.class_per]
                    elif gamer.users == max_users:
                        winner.append(gamer.name + " " + gamer.class_per)
                self.print_boards()
                self.final(", ".join(winner))

            num_sprint += 1

    pass
