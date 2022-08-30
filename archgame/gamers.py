from archgame import obj
from archgame import cli
from archgame import constants


class InvalidUserInput(Exception):
    pass


class Gamer:
    def __init__(self, n, cl, flag_slow_print):
        self.board = obj.Board()
        self.cli = cli.Cli(flag_slow_print)
        self.name = n
        self.class_per = cl
        # Где-нибудь решить, что делать с классом - передавать его в боард
        # для счета капасити прогеру или здесь эту логику сделать...
        if self.is_proger:
            self.board.lim_a = constants.LIM_A_P
        else:
            # API может выдержать до 3к нагрузки
            self.board.lim_a = constants.LIM_A
        self.q_point = constants.FIRST_SPRINT_POINTS
        self.users = 0

    @property
    def is_cli(self):
        if isinstance(self.cli, cli.Cli):
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
        for choice in choices:
            if '-' in choice:
                input_list = choice.split('-')
                if len(input_list) != 3:
                    raise InvalidUserInput
                _, component, num_cell = choice.split('-')
                if not num_cell.isdigit():
                    raise InvalidUserInput
                num_cell = int(num_cell)
                if component not in constants.POSSIBLE_INPUTS:
                    raise InvalidUserInput
                if 0 > num_cell or num_cell > constants.SIZE_BOARD ** 2 + 1:
                    raise InvalidUserInput

            elif choice != '1':
                raise InvalidUserInput

    def action(self):
        while True:
            try:
                inpt_str = self.cli.ask(self.name)
                choices = inpt_str.split(',')
                self.validate_input_user(choices)
                ans = [0, []]
                for i in choices:
                    if i[0] == "1":  # добавить юзеров
                        ans[0] += 1
                    if i[0] == "2":  # добавить компонент
                        two, comp, number = i.strip().split("-")
                        ans[1].append([comp, int(number)])
                add_u, add_c = ans
                for i in add_c:
                    component, num = i
                    self.board.change_component(component, num)
                self.users = min(
                    (add_u + self.users),
                    self.board.cap(
                        self.board.quantity_component(
                            constants.API),
                        self.board.quantity_component(
                            constants.DB),
                        self.board.quantity_component(
                            constants.LB)))
                return ()
            except InvalidUserInput:
                self.cli.output_print_msg(
                    'Некорректный ввод, пожалуйста, попробуйте снова,\n'
                    'Помните, что на ход вам даётся %d очка' %
                    self.q_point)

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
