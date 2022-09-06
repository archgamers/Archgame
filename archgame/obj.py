from archgame import constants


# Номер, который передается в функцию - это номер ячейки на поле! НЕ в массиве
# и возвращается отсюда тоже он!.


class Board:
    def __init__(self):
        self.board = [constants.EMPTY_CELL] * (constants.SIZE_BOARD ** 2)

        # Компоненты
        self.lim_a = constants.LIM_A  # API может выдержать до 3к нагрузки
        self.lim_d = constants.LIM_D  # DB может поддерживать до 3х API
        self.lim_l = constants.LIM_L  # LB может обслуживать не больше 3х API
        # В случае потери DB при возврате ее назад бэкап позволяет вернуть
        # часть пользовательской базы, но не более стольких к.
        self.lim_b = constants.LIM_B

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
