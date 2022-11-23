# -*-coding: utf-8 -*-
import logging

from archgame import events as game_events
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
                self.gamers[num].print_message(texts.EVENT_FAILED)
            self.gamers[num].class_benefit()

    def begin(self, num_sprint, show_blank_lines=True):
        if show_blank_lines:
            self.print_all('\n\n\n')
        if num_sprint == 1:
            self.print_all(texts.SPRINTS % num_sprint + "\n" +
                           texts.DESC % constants.FIRST_SPRINT_POINTS)
        else:
            self.print_all(texts.SPRINTS % num_sprint + "\n" +
                           texts.DESC % constants.LIM_POINTS)

    def print_boards(self):
        all_boards = []
        for gamer in self.gamers:
            all_boards.append(gamer.print_board())

        for first_line_all_boards in zip(*all_boards):
            self.print_all("".join(first_line_all_boards).strip())

    def final(self, winner):
        self.print_all(texts.ENDING % winner)

    def end_game(self):
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
        return winner

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
                winner = self.end_game()

            num_sprint += 1


class TelegramGameServer(GameServer):
    def __init__(self, game_uuid, gamers=None, events=None, game_owner=None):
        events = events or game_events.Events()
        super(TelegramGameServer, self).__init__(
            gamers=gamers or [],
            events=events,
        )
        self._status = constants.GAME_INIT_ST
        self._uuid = game_uuid
        self.log = logging.getLogger(__name__)
        self.num_sprint = 1
        self._game_owner = game_owner

    @property
    def status(self):
        return self._status

    @property
    def game_owner(self):
        if self._game_owner:
            return self._game_owner
        elif self.gamers:
            return self.gamers[0]
        else:
            return None

    @property
    def game_uuid(self):
        return self._uuid

    def print_boards(self):
        all_triple = []
        acc = 0
        triple = []
        for gamer in self.gamers:
            triple += [gamer.print_board()]
            if acc == 3:
                all_triple.append(triple)
                acc = 0
                triple = []
        if len(triple) > 0:
            all_triple.append(triple)

        text = ""
        for triple in all_triple:
            for first_line_all_boards in zip(*triple):
                text += ("".join(first_line_all_boards).strip()) + "\n"

        self.print_all("<pre>" + text + "</pre>")

    def set_status(self, new_status):
        self.log.debug('Set status %s for game %s', new_status, self.game_uuid)
        self._status = new_status

    def start_game(self):
        self.set_status(constants.GAME_START_ST)
        self._set_users_waiting()
        self.run_sprint()

    def _set_users_waiting(self):
        for gamer in self.gamers:
            if not gamer.is_bot:
                gamer.set_status(constants.USER_WAIT_ST)

    def run_sprint(self):
        self.begin(self.num_sprint, show_blank_lines=False)
        self.print_boards()

    def end_sprint(self):
        for gamer in self.gamers:
            gamer.default_points()

        self.print_boards()

        self.events_run()
        for gamer in self.gamers:
            gamer.check_user()

        self._set_users_waiting()

    def check_sprint_next_step(self):
        for gamer in self.gamers:
            if gamer.status != constants.USER_READY_ST:
                return

        for gamer in self.gamers:
            if gamer.is_bot:
                gamer.action()

        self.end_sprint()

        if self.num_sprint == constants.WIN_SCORE:
            self.end_game()
            self.set_status(constants.GAME_END_ST)
            return

        self.num_sprint += 1
        self.run_sprint()

    def add_gamer(self, gamer):
        gamer.game_uuid = self.game_uuid
        self.log.debug('Add player %s in game %s', gamer.name, self.game_uuid)
        self.gamers.append(gamer)

    def main_cycle(self):
        return NotImplemented

    def events_run(self):
        for num in range(len(self.gamers)):
            try:
                self.events.random_event(self.gamers, num,
                                         ouput_func=self.print_all)
            except Exception:
                self.gamers[num].print_message(texts.EVENT_FAILED)
            self.gamers[num].class_benefit()
