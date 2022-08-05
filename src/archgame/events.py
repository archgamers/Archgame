from archgame import texts
from archgame import constants
import random

#Во все события передавать всё одинаково!
#Когда буду делать отображение надписей для событий - передавать во все объект Cli ещё!!!

# убрать бэкап, если есть, нет - 0 u
def dba(boards, num, gui):
    board = boards[num]
    if board.is_a_component(constants.BCKP):
        board.del_component(random.choice(board.all_nums_component(constants.BCKP)))
    else:
        board.users = 0
    gui.cli_print([boards[num].name + ":", texts.TEXT_DBA])


def del_api(boards, num, gui):
    board = boards[num]
    num_rand_comp = random.choice(board.all_nums_component(constants.API))
    board.del_component(num_rand_comp)
    gui.cli_print([boards[num].name + ":", texts.TEXT_DEL_API % num_rand_comp])

#Добавляет апи на пустое место
def add_random_api(boards, num, gui):
    board = boards[num]
    board.change_component(constants.API, random.choice(board.all_nums_component(constants.EMPTY_CELL)))
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_RANDOM_API])

def add_random_db(boards, num, gui):
    board = boards[num]
    board.change_component(constants.DB, random.choice(board.all_nums_component(constants.EMPTY_CELL)))
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_RANDOM_DB])

def add_random_lb(boards, num, gui):
    board = boards[num]
    board.change_component(constants.LB, random.choice(board.all_nums_component(constants.EMPTY_CELL)))
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_RANDOM_LB])

def drop_cell(boards, num, gui):
    board = boards[num]
    num_cell = random.randint(1, constants.SIZE_BOARD**2)
    board.del_component(num_cell)
    gui.cli_print([boards[num].name + ":", texts.TEXT_DROP_CELL % num_cell])

def bankrupt(boards, num, gui):
    constants.BANKRUPT = True
    constants.BANKRUPT_NAME = boards[num].name
    gui.cli_print([boards[num].name + ":", texts.TEXT_BANKRUPT])


def admin_error(boards, num, gui):
    b = boards[num]
    new_b = [constants.EMPTY_CELL] * (constants.SIZE_BOARD**2)
    l_step = 0
    for ost in range(constants.SIZE_BOARD-1, 0-1, -1):
        for old_b_num in range(ost, constants.SIZE_BOARD**2, 4):
            new_b[l_step] = b.board[old_b_num]
            l_step += 1
    boards[num].board = new_b
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADMIN_ERROR])


def add_1k(boards, num, gui):
    board = boards[num]
    b_cap = board.cap(board.quantity_component(constants.API), board.quantity_component(constants.DB), board.quantity_component(constants.LB))
    if b_cap < board.users+1:
        board.change_users(-1)
    else:
        board.change_users(1)
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_1K])

def add_2k(boards, num, gui):
    board = boards[num]
    b_cap = board.cap(board.quantity_component(constants.API), board.quantity_component(constants.DB), board.quantity_component(constants.LB))
    if b_cap < board.users+1:
        board.change_users(-1)
    else:
        board.change_users(2)
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_2K])


def add_3k(boards, num, gui):
    board = boards[num]
    b_cap = board.cap(board.quantity_component(constants.API), board.quantity_component(constants.DB), board.quantity_component(constants.LB))
    if b_cap < board.users+1:
        board.change_users(-1)
    else:
        board.change_users(3)
    gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_3K])


def drop_component(boards, num, gui):
    nums_comps = (boards[num].all_nums_component(constants.API) +
                  boards[num].all_nums_component(constants.DB) +
                  boards[num].all_nums_component(constants.LB) +
                  boards[num].all_nums_component(constants.BCKP))
    num_comp = random.choice(nums_comps)
    boards[num].del_component(num_comp)
    gui.cli_print([boards[num].name + ":", texts.TEXT_DROP_COMPONENT % num_comp])

def left_right_1k(boards, num, gui):
    boards[num].change_users(-2)
    if num == len(boards) - 1:
        boards[0].change_users(1)
        boards[num-1].change_users(1)
    elif num == 0:
        boards[len(boards)-1].change_users(1)
        boards[num + 1].change_users(1)
    else:
        boards[num - 1].change_users(1)
        boards[num + 1].change_users(1)
    gui.cli_print([boards[num].name + ":", texts.TEXT_LEFT_RIGHT_1K])


def drop_rack(boards, num, gui):
    # фактически генерим номер стойки
    n = random.randint(1,4)
    for i in range(n, constants.SIZE_BOARD**2+1, 4):
        boards[num].del_component(i)
    gui.cli_print([boards[num].name + ":", texts.TEXT_DROP_RACK, "№" + str(n)])


def right_component(boards, num, gui):
    nums_comps = (boards[num].all_nums_component(constants.API) +
                  boards[num].all_nums_component(constants.DB) +
                  boards[num].all_nums_component(constants.LB) +
                  boards[num].all_nums_component(constants.BCKP))
    num_comp = random.choice(nums_comps)
    comp = boards[num].board[num_comp-1]
    boards[num].del_component(num_comp)
    if num == len(boards)-1: num_new_board = 0
    else: num_new_board = num + 1
    num_new_comp = random.choice(boards[num_new_board].all_nums_component(constants.EMPTY_CELL))
    boards[num_new_board].change_component(comp, num_new_comp)
    gui.cli_print([boards[num].name + ":", texts.TEXT_RIGHT_COMPONENT % num_new_comp])


class Events:
    def __init__(self):
        self.events = []
        self.refill_events()

    def refill_events(self):
        self.events = (
        [dba] * constants.CHANCE_DBA +
        [del_api] * constants.CHANCE_DEL_API +
        [add_random_api] * constants.CHANCE_ADD_RANDOM_API +
        [add_random_db] * constants.CHANCE_ADD_RANDOM_DB +
        [add_random_lb] * constants.CHANCE_ADD_RANDOM_LB +
        [drop_cell] * constants.CHANCE_DROP_CELL +
        [bankrupt] * constants.CHANCE_BANKRUPT +
        [admin_error] * constants.CHANCE_ADMIN_ERROR +
        [add_1k] * constants.CHANCE_ADD_1K +
        [add_2k] * constants.CHANCE_ADD_2K +
        [add_3k] * constants.CHANCE_ADD_3K +
        [drop_component] * constants.CHANCE_DROP_COMPONENT +
        [left_right_1k] * constants.CHANCE_LEFT_RIGHT_1K +
        [drop_rack] * constants.CHANCE_DROP_RACK +
        [right_component] * constants.CHANCE_RIGHT_COMPONENT
        )
        random.shuffle(self.events)
        return self.events

    def random_event(self, boards, num, gui):
        try:
            random_ev = self.events.pop()
        except IndexError:
            self.events = self.refill_events()
            random_ev = self.events.pop()
        random_ev(boards, num, gui)
