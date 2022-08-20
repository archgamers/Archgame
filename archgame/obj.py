from archgame import constants

# Номер, который передается в функцию - это номер ячейки на поле! НЕ в массиве
# и возвращается отсюда тоже он!.


class Player:
    def __init__(self, name, class_p):
        self.name = name
        self.users = 0
        self.board = [constants.EMPTY_CELL] * (constants.SIZE_BOARD**2)
        self.class_per = class_p

        # Компоненты
        if self.is_proger:
            self.lim_a = constants.LIM_A_P
        else:
            self.lim_a = constants.LIM_A  # API может выдержать до 3к нагрузки
        self.lim_d = constants.LIM_D  # DB может поддерживать до 3х API
        self.lim_l = constants.LIM_L  # LB может обслуживать не больше 3х API
        # В случае потери DB при возврате ее назад бэкап позволяет вернуть
        # часть пользовательской базы, но не более стольких к.
        self.lim_b = constants.LIM_B

        self.q_point = constants.FIRST_SPRINT_POINTS

    def default_points(self):
        self.q_point = constants.LIM_POINTS

    def bankrupt_points(self):
        self.q_point = constants.BANKRUPT_POINTS

    @property
    def is_admin(self):
        if self.class_per in ["А", "A", "a", "а"]:
            return True
        return False

    @property
    def is_manager(self):
        if self.class_per in ["М", "M", "m", "м"]:
            return True
        return False

    @property
    def is_proger(self):
        if self.class_per in ["Р", "P", "p", "р"]:
            return True
        return False

    # НУЖЕН ДЛЯ ГЕНЕРАТОРА!
    # На начло игры на всех полях стандартное расположение 1 A, 6 D, 11 B; u 1
    def default(self):
        self.board[1 - 1] = constants.API
        self.board[6 - 1] = constants.DB
        self.board[11 - 1] = constants.BCKP
        self.users = 1

    def class_benefit(self):
        if self.is_admin:
            pass
        if self.is_manager:
            self.users += 1
        if self.is_proger:
            pass

    def change_users(self, number):
        self.users += number
        if self.users < 0:
            self.users = 0

    def change_component(self, comp, num):
        self.board[num - 1] = comp

    def del_component(self, num):
        self.board[num - 1] = constants.EMPTY_CELL

    def quantity_component(self, comp):
        return self.board.count(comp)

    def is_a_component(self, comp):
        return comp in self.board

    # ввернет список всех номеров компонента
    def all_nums_component(self, comp):
        nums = []
        for i in range(len(self.board)):
            if self.board[i] == comp:
                nums.append(i + 1)
        return nums

    # если путо - True, если нет - False
    def is_cell_empty(self, num):
        if self.board[num - 1] == constants.EMPTY_CELL:
            return True
        else:
            return False

    def cap(self, q_A, q_D, q_L):
        return self.lim_a * min((q_D * self.lim_d),
                                min(max(1, q_L * self.lim_l), q_A))
