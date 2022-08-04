from archgame import texts
from archgame import constants
import random

#Во все события передавать всё одинаково!
#Когда буду делать отображение надписей для событий - передавать во все объект Cli ещё!!!

# убрать бэкап, если есть, нет - 0 u
def dba(boards, num):
    board = boards[num]
    if board.is_a_component(texts.BCKP):
        board.del_component(random.choice(board.all_nums_component(texts.BCKP)))
    else:
        board.users = 0


def del_api(boards, num):
    board = boards[num]
    board.del_component(random.choice(board.all_nums_component(texts.API)))

def bankrupt():
    pass

#Добавляет апи на пустое место
def add_random_api(boards, num):
    board = boards[num]
    board.change_component(texts.API, random.choice(board.all_nums_component(texts.EMPTY_CELL)))

def add_random_db(boards, num):
    board = boards[num]
    board.change_component(texts.DB, random.choice(board.all_nums_component(texts.EMPTY_CELL)))

def add_random_lb(boards, num):
    board = boards[num]
    board.change_component(texts.LB, random.choice(board.all_nums_component(texts.EMPTY_CELL)))

def drop_cell(boards, num):
    board = boards[num]
    num = random.randint(1, constants.SIZE_BOARD**2)
    board.del_component(num)

def admin_error():
    pass

def add_1k():
    pass

def add_2k():
    pass

def add_3k():
    pass

events = (
    [dba] * 5 +
    [del_api] * 3 +
    [add_random_api] +
    [add_random_db] +
    [add_random_lb] +
    [drop_cell]
)

random.shuffle(events)

def random_event(boards, num):
    random_ev = events.pop()
    random_ev(boards, num)
