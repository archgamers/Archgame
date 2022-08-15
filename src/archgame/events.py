from archgame import texts
from archgame import constants
import random

import inspect
import sys


#Во все события передавать всё одинаково!
#Когда буду делать отображение надписей для событий - передавать во все объект Cli ещё!!!


class BaseEvent(object):
    short_name = ''
    cards_count = 1

    def apply(self, boards, num, gui):
        raise NotImplementedError()


# убрать бэкап, если есть, нет - 0 u
class DbaEvent(BaseEvent):
    cards_count = 3

    def apply(self, boards, num, gui):
        board = boards[num]
        if board.is_a_component(constants.BCKP):
            board.del_component(random.choice(board.all_nums_component(constants.BCKP)))
        else:
            board.users = 0
        gui.cli_print([boards[num].name + ":", texts.TEXT_DBA])


class DelApiEvent(BaseEvent):
    def apply(self, boards, num, gui):
        board = boards[num]
        num_rand_comp = random.choice(board.all_nums_component(constants.API))
        board.del_component(num_rand_comp)
        gui.cli_print([boards[num].name + ":", texts.TEXT_DEL_API % num_rand_comp])



class AddRandomAPIEvent(BaseEvent):
    component = constants.API
    text = texts.TEXT_ADD_RANDOM_API

    def apply(self, boards, num, gui):
        board = boards[num]
        board.change_component(self.component, random.choice(board.all_nums_component(constants.EMPTY_CELL)))
        gui.cli_print([boards[num].name + ":", self.text])


class AddRandomDBEvent(AddRandomAPIEvent):
    component = constants.DB
    text = texts.TEXT_ADD_RANDOM_DB


class AddRandomLBEvent(AddRandomAPIEvent):
    component = constants.LB
    text = texts.TEXT_ADD_RANDOM_LB


class DropCellEvent(BaseEvent):
    def apply(self, boards, num, gui):
        board = boards[num]
        num_cell = random.randint(1, constants.SIZE_BOARD**2)
        board.del_component(num_cell)
        gui.cli_print([boards[num].name + ":", texts.TEXT_DROP_CELL % num_cell])


class BankruptEvent(BaseEvent):
    def apply(self, boards, num, gui):
        # TODO(g.melikov): this should not be a global variable
        constants.BANKRUPT = True
        constants.BANKRUPT_NAME = boards[num].name
        gui.cli_print([boards[num].name + ":", texts.TEXT_BANKRUPT])


class AdminErrorEvent(BaseEvent):
    def apply(self, boards, num, gui):
        b = boards[num]
        new_b = [constants.EMPTY_CELL] * (constants.SIZE_BOARD**2)
        l_step = 0
        for ost in range(constants.SIZE_BOARD-1, 0-1, -1):
            for old_b_num in range(ost, constants.SIZE_BOARD**2, 4):
                new_b[l_step] = b.board[old_b_num]
                l_step += 1
        boards[num].board = new_b
        gui.cli_print([boards[num].name + ":", texts.TEXT_ADMIN_ERROR])


class BonusEvent(BaseEvent):
    amount = 1
    penalty = 1

    def apply(self, boards, num, gui):
        board = boards[num]
        b_cap = board.cap(board.quantity_component(constants.API), board.quantity_component(constants.DB), board.quantity_component(constants.LB))
        if b_cap < board.users+self.amount:
            board.change_users(-self.penalty)
        else:
            board.change_users(self.amount)
        gui.cli_print([boards[num].name + ":", texts.TEXT_ADD_AMOUNT % (self.amount, self.amount)])


class Bonus2Event(BonusEvent):
    amount = 2
    penalty = 1


class Bonus3Event(BonusEvent):
    amount = 3
    penalty = 1
    cards_count = 2


class DropComponentEvent(BaseEvent):
    def apply(self, boards, num, gui):
        nums_comps = (boards[num].all_nums_component(constants.API) +
                      boards[num].all_nums_component(constants.DB) +
                      boards[num].all_nums_component(constants.LB) +
                      boards[num].all_nums_component(constants.BCKP))
        num_comp = random.choice(nums_comps)
        boards[num].del_component(num_comp)
        gui.cli_print([boards[num].name + ":", texts.TEXT_DROP_COMPONENT % num_comp])


class MoveComplonentToCompetitorEvent(BaseEvent):
    def apply(self, boards, num, gui):
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


class DropRackEvent(BaseEvent):
    cards_count = 2

    def apply(self, boards, num, gui):
        # фактически генерим номер стойки
        n = random.randint(1, 4)
        for i in range(n, constants.SIZE_BOARD**2+1, 4):
            boards[num].del_component(i)
        gui.cli_print([boards[num].name + ":", texts.TEXT_DROP_RACK, "№" + str(n)])


class ComponentToRightCompetitorEvent(BaseEvent):
    def apply(self, boards, num, gui):
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


clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
game_events = [event[1] for event in clsmembers if issubclass(event[1],
               BaseEvent) and event[1] is not BaseEvent]


class Events:
    def __init__(self):
        self.events = []
        self.refill_events()

    def refill_events(self):
        self.events = []
        for event in game_events:
            self.events.extend([event] * event.cards_count)
        random.shuffle(self.events)
        return self.events

    def random_event(self, boards, num, gui):
        try:
            random_ev = self.events.pop()
        except IndexError:
            self.events = self.refill_events()
            random_ev = self.events.pop()
        random_ev().apply(boards, num, gui)
