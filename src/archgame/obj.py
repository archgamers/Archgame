from archgame import texts
from archgame import constants

#Номер, который передается в функцию - это номер ячейки на поле! НЕ в массиве
# и возвращается отсюда тоже он!.
class Player:
    def __init__(self, name, class_p):
        self.name = name
        self.users = 1
        self.board = [constants.EMPTY_CELL] * (constants.SIZE_BOARD**2)
        self.class_per = class_p

    #На начло игры на всех полях стандартное расположение 1 A, 6 D, 11 B; u 1
    def default(self):
        self.board[1-1] = constants.API
        self.board[6 - 1] = constants.DB
        self.board[11 - 1] = constants.BCKP
        self.users = 1

    def change_users(self, number):
        self.users += number

    def change_component(self, comp, num):
        self.board[num-1] = comp

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
            if self.board[i] == comp: nums.append(i+1)
        return(nums)

    # если путо - True, если нет - False
    def is_cell_empty(self,num):
        if self.board[num-1] == constants.EMPTY_CELL:
            return True
        else:
            return False

    def cap(self, q_A, q_D, q_L):
        return constants.LIM_A * min( (q_D * constants.LIM_D) , min( max(1, q_L * constants.LIM_L) , q_A) )
