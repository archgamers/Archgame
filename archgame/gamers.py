# -*-coding: utf-8 -*-
import logging
import random

from archgame import obj
from archgame import cli
from archgame import constants
from archgame import texts


class InvalidUserInput(Exception):
    pass


class Gamer:
    def __init__(self, name, class_per="", flag_slow_print=False, g_cli=None):
        self.users = 0
        self.q_point = constants.FIRST_SPRINT_POINTS
        self.board = obj.Board()
        self.name = name
        self.class_per = class_per
        self.cli = g_cli or cli.Cli(flag_slow_print)
        # Где-нибудь решить, что делать с классом - передавать его в боард
        # для счета капасити прогеру или здесь эту логику сделать...
        if self.is_proger:
            self.board.lim_a = constants.LIM_A_P
        else:
            # API может выдержать до 3к нагрузки
            self.board.lim_a = constants.LIM_A

    @property
    def is_bot(self):
        return False

    @property
    def is_cli(self):
        if type(self.cli) == cli.Cli:
            return True
        return False

    @property
    def is_admin(self):
        if self.class_per == "A":
            return True
        return False

    @property
    def is_manager(self):
        if self.class_per == "M":
            return True
        return False

    @property
    def is_proger(self):
        if self.class_per == "P":
            return True
        return False

    @property
    def caps(self):
        return self.board.cap(
                        self.board.quantity_component(
                            constants.API),
                        self.board.quantity_component(
                            constants.DB),
                        self.board.quantity_component(
                            constants.LB))

    def default_component_name(self, comp):
        if comp in ["A", "a"]:
            return constants.API
        if comp in ["D", "d"]:
            return constants.DB
        if comp in ["L", "l"]:
            return constants.LB
        if comp in ["B", "b"]:
            return constants.BACKUP

    def set_class(self, cl):
        if cl in constants.ALL_CLASSES:
            self.class_per = cl

    def get_class(self):
        return self.class_per

    def default_points(self):
        self.q_point = constants.LIM_POINTS

    def bankrupt_points(self):
        self.q_point = constants.BANKRUPT_POINTS

    def class_benefit(self):
        if self.is_admin:
            pass
        if self.is_manager:
            self.users += 1
        if self.is_proger:
            pass

    # @staticmethod
    def validate_input_user(self, choices):
        if len(choices) != self.q_point:
            raise InvalidUserInput
        for orig_choice in choices:
            choice = orig_choice.strip(constants.SEPARATOR)
            if constants.SEPARATOR_COMPONENTS in choice:
                input_list = choice.split(constants.SEPARATOR_COMPONENTS)
                if len(input_list) != 3:
                    raise InvalidUserInput
                _, component, num_cell = choice.split(
                    constants.SEPARATOR_COMPONENTS)
                if not num_cell.isdigit():
                    raise InvalidUserInput
                num_cell = int(num_cell)
                if component not in constants.POSSIBLE_INPUT_COMPONENTS:
                    raise InvalidUserInput
                if 0 > num_cell or num_cell > (constants.SIZE_BOARD ** 2):
                    raise InvalidUserInput

            elif choice not in constants.CMD_INPUT_USER:
                raise InvalidUserInput

    def set_new_users(self, users):
        self.users = min(
            (users + self.users),
            self.board.cap(
                self.board.quantity_component(constants.API),
                self.board.quantity_component(constants.DB),
                self.board.quantity_component(constants.LB)
            )
        )

    def action(self):
        while True:
            try:
                input_str = self.cli.ask(self.name)
                choices = input_str.split(constants.SEPARATOR)
                self.validate_input_user(choices)
                ans = [0, []]
                for i in choices:
                    # добавить юзеров
                    if i[0] in constants.CMD_INPUT_USER:
                        ans[0] += 1
                    # добавить компонент
                    if i[0] in constants.CMD_INPUT_SERVICE:
                        two, comp, number = i.strip().split(
                            constants.SEPARATOR_COMPONENTS)
                        ans[1].append([self.default_component_name(comp),
                                       int(number)])
                add_u, add_c = ans
                for i in add_c:
                    component, num = i
                    self.board.change_component(component, num)
                self.set_new_users(add_u)
                return ()
            except InvalidUserInput:
                self.cli.output_print_msg(
                    texts.INVALID_USER_INPUT % self.q_point)

    def print_message(self, texts):
        self.cli.output_print_msg(texts)

    def input_message(self, texts):
        self.cli.output_input_msg(texts)

    def print_board(self):
        return self.cli.print_board(self.board, self.name,
                                    self.class_per, self.users,
                                    self.cap(
                                        self.quantity_component(constants.API),
                                        self.quantity_component(constants.DB),
                                        self.quantity_component(constants.LB)))

    def check_user(self):
        self.users = min(
            self.users, self.board.cap(
                self.board.quantity_component(
                    constants.API), self.board.quantity_component(
                    constants.DB), self.board.quantity_component(
                    constants.LB)))

    def change_users(self, number):
        self.users += number
        if self.users < 0:
            self.users = 0

    def change_component(self, comp, num):
        return self.board.change_component(comp, num)

    def del_component(self, num):
        return self.board.del_component(num)

    def quantity_component(self, comp):
        return self.board.quantity_component(comp)

    def is_a_component(self, comp):
        return self.board.is_a_component(comp)

    # ввернет список всех номеров компонента
    def all_nums_component(self, comp):
        return self.board.all_nums_component(comp)

    # если пусто - True, если нет - False
    def is_cell_empty(self, num):
        return self.board.is_cell_empty(num)

    def cap(self, q_A, q_D, q_L):
        return self.board.cap(q_A, q_D, q_L)

    def return_comp(self, num):
        return self.board.board[num]


class Bot(Gamer):
    def __init__(self, num, cl, flag_slow_print=False, g_cli=None):
        super(Bot, self).__init__("Bot" + str(num),
                                  cl,
                                  flag_slow_print=flag_slow_print,
                                  g_cli=g_cli)

    @property
    def is_bot(self):
        return True

    # Считает разницу между количеством юзеров и своим капасити
    def users_vs_caps(self):
        return abs(self.users - self.cap(
            self.quantity_component(constants.API),
            self.quantity_component(constants.DB),
            self.quantity_component(constants.LB)))

    # Случайная пустая ячейка
    def random_empty_cell(self):
        cells = self.all_nums_component(constants.EMPTY_CELL)
        if cells == []:
            return random.randint(0, constants.SIZE_BOARD**2)
        return random.choice(cells)

    # Все ф-ции logic_ содержат в себе логику траты 1 очка
    # Менеджер: сначала наращивает капасити максимально(примерно до 18),
    # потом начинает добавлять себе юзеров
    def logic_manager(self):
        q_A = self.quantity_component(constants.API)
        q_D = self.quantity_component(constants.DB)
        q_L = self.quantity_component(constants.LB)
        q_B = self.quantity_component(constants.BACKUP)
        if q_D < 1:
            self.change_component(constants.DB, self.random_empty_cell())
        elif q_A < 1:
            self.change_component(constants.API, self.random_empty_cell())
        elif q_B < 1:
            self.change_component(constants.BACKUP, self.random_empty_cell())
        elif q_A < 2:
            self.change_component(constants.API, self.random_empty_cell())
        elif q_L < 1:
            self.change_component(constants.LB, self.random_empty_cell())
        elif q_A < 3:
            self.change_component(constants.API, self.random_empty_cell())
        elif q_D < 2:
            self.change_component(constants.DB, self.random_empty_cell())
        elif q_L < 2:
            self.change_component(constants.LB, self.random_empty_cell())
        elif q_A < 6:
            self.change_component(constants.API, self.random_empty_cell())
        else:
            self.change_users(1)

    # Админ: наращивает капасити до 6, добавляет юзеров до 3,
    # наращивает капасити до 9, добавляет юзеров до 6
    # и т.д до капасити 18, после этого просто +юзеры
    # в отличие от прогера не тратит очки на бэкапы
    def logic_admin(self):
        q_A = self.quantity_component(constants.API)
        q_D = self.quantity_component(constants.DB)
        q_L = self.quantity_component(constants.LB)
        if q_D < 1:
            self.change_component(constants.DB, self.random_empty_cell())
        elif q_A < 1:
            self.change_component(constants.API, self.random_empty_cell())
        elif q_L < 1:
            self.change_component(constants.LB, self.random_empty_cell())
        elif q_A < 2:
            self.change_component(constants.API, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_A < 3:
            self.change_component(constants.API, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_D < 2:
            self.change_component(constants.DB, self.random_empty_cell())
        elif q_L < 2:
            self.change_component(constants.LB, self.random_empty_cell())
        elif q_A < 4:
            self.change_component(constants.API, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_A < 5:
            self.change_component(constants.API, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_A < 6:
            self.change_component(constants.API, self.random_empty_cell())
        else:
            self.change_users(1)

    # Программист: наращивает капасити до 5, добавляет юзеров до 2,
    # наращивает капасити до 10, добавляет юзеров до 7
    # и т.д до капасити 20, после этого просто +юзеры
    def logic_proger(self):
        q_A = self.quantity_component(constants.API)
        q_D = self.quantity_component(constants.DB)
        q_L = self.quantity_component(constants.LB)
        q_B = self.quantity_component(constants.BACKUP)
        if q_D < 1:
            self.change_component(constants.DB, self.random_empty_cell())
        elif q_A < 1:
            self.change_component(constants.API, self.random_empty_cell())
        elif q_B < 1:
            self.change_component(constants.BACKUP, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_A < 2:
            self.change_component(constants.API, self.random_empty_cell())
        elif q_L < 1:
            self.change_component(constants.LB, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_D < 2:
            self.change_component(constants.DB, self.random_empty_cell())
        elif q_L < 2:
            self.change_component(constants.LB, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_A < 3:
            self.change_component(constants.API, self.random_empty_cell())
        elif self.users_vs_caps() > 3:
            self.change_users(1)
        elif q_A < 4:
            self.change_component(constants.API, self.random_empty_cell())
        else:
            self.change_users(1)

    # Содержит логику ходов бота
    def action(self):
        if self.q_point == 4:
            self.default_start()
            return 0
        points = self.q_point
        while points != 0:
            if self.is_manager:
                self.logic_manager()
            if self.is_admin:
                self.logic_admin()
            if self.is_proger:
                self.logic_proger()
            points -= 1

    # Дефолтное расположение, для первого хода бота
    def default_start(self):
        self.board.change_component(constants.API, 1)
        self.board.change_component(constants.DB, 6)
        # Если это админ, то бэкап ему не нужен, ставим балансер
        if self.is_admin:
            self.board.change_component(constants.LB, 11)
        else:
            self.board.change_component(constants.BACKUP, 11)
        self.board.change_component(constants.API, 16)


class TelegaBot(Bot):
    def __init__(self, num, cl, flag_slow_print=False, g_cli=None):
        super(TelegaBot, self).__init__(
            num=num,
            cl=cl,
            flag_slow_print=flag_slow_print,
            g_cli=g_cli or cli.BotIO(False)
        )
        self.status = "ready"
        self.user_id = None
        self.game_uuid = None


class TelegaGamer(Gamer):
    def __init__(self, name, user_id, game_uuid, class_per="",
                 flag_slow_print=False, g_cli=None):
        super(TelegaGamer, self).__init__(name,
                                          class_per=class_per,
                                          flag_slow_print=flag_slow_print,
                                          g_cli=g_cli)
        self.user_id = user_id
        self.game_uuid = game_uuid
        self._status = constants.USER_INIT_ST
        self.log = logging.getLogger(__name__)

    @property
    def status(self):
        return self._status

    def set_status(self, new_status):
        self.log.debug('Set status %s for user %s', new_status, self.user_id)
        self._status = new_status

    def set_user_input(self, text):
        if self.status == constants.USER_WAIT_ST:
            self.action(text)

    def action(self, text):
        self.log.debug('Working with user %s input: "%s"', self.user_id, text)
        try:
            choices = text.split(constants.SEPARATOR)
            self.validate_input_user(choices)
            ans = [0, []]
            for i in choices:
                if i[0] in constants.CMD_INPUT_USER:  # добавить юзеров
                    ans[0] += 1
                if i[0] in constants.CMD_INPUT_SERVICE:  # добавить компонент
                    two, comp, number = i.strip().split(
                        constants.SEPARATOR_COMPONENTS)
                    ans[1].append([self.default_component_name(comp),
                                   int(number)])
            add_u, add_c = ans
            for i in add_c:
                component, num = i
                self.board.change_component(component, num)
            self.set_new_users(add_u)
            self.set_status(constants.USER_READY_ST)
        except InvalidUserInput:
            self.log.debug('Found invalid user input for %s: "%s"',
                           self.user_id, text)
            self.cli.output_print_msg(
                texts.INVALID_USER_INPUT % self.q_point)
