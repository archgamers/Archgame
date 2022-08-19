from archgame import constants
import random

import inspect
import sys


#Во все события передавать всё одинаково!
#Когда буду делать отображение надписей для событий - передавать во все объект Cli ещё!!!


class BaseEvent(object):
    short_text = ''
    long_text = ''
    immunity_text = ''
    cards_count = 1

    @property
    def random_long_text(self):
        if type(self.long_text) == list:
            return random.choice(self.long_text)
        return self.long_text

    def apply(self, boards, num):
        # If applied - return True or tuple which will be formatted into
        #   output string.
        raise NotImplementedError()

    def act(self, boards, num, gui):
        result = self.apply(boards, num)
        response = [boards[num].name + ":", self.random_long_text]
        if result is None:
            response.append(self.immunity_text)
        else:
            response.append(self.short_text % result
                            if result is not True else self.short_text)
        gui.cli_print(response)


# убрать бэкап, если есть, нет - 0 u
class DbaEvent(BaseEvent):
    cards_count = 3
    short_text = '''Все данные потеряны, а вместе с ними - и клиенты.'''
    long_text = '''Ваш аутсорсер-DBA в общем чате:
- начинаю работы по переносу реплики, аффекта не ожидается
...
...
...
- при переносе реплики я потерял таблицу. данных больше нет.'''
    immunity_text = '''Либо вы делаете бекапы, либо вы УЖЕ делаете бекапы,
минус бекап, но база восстановлена.'''

    def apply(self, boards, num):
        board = boards[num]
        if board.is_admin:
            self.long_text = '''Ваш аутсорсер-DBA почти удалил таблицу, но вы вовремя дали ему по шапке и успешно сделали всё сами.'''
            self.short_text = '''Данные спасены.'''
            self.immunity_text = ''
            pass
        else:
            if board.is_a_component(constants.BCKP):
                board.del_component(
                    random.choice(board.all_nums_component(constants.BCKP)))
                return None
            else:
                board.users = 0
                return True


class DelApiEvent(BaseEvent):
    short_text = 'API №%i потеряна.'
    long_text = '''Вам повезло, хабра-эффект принёс много клиентов!
...
Но одна из API не выдержала и взорвалась :('''

    def apply(self, boards, num):
        board = boards[num]
        num_rand_comp = random.choice(board.all_nums_component(constants.API))
        board.del_component(num_rand_comp)
        return num_rand_comp


class AddRandomAPIEvent(BaseEvent):
    component = constants.API
    component_name = 'API'
    long_text = ['''\
Произошло ужасное - соседнее подразделение разогнали.
Целый спринт вы ждали худшего и ходили по собеседованиям.
...
...
В итоге выяснилось, что коллег перевели на другое направление, а вам достался
один из их компонентов :)''',
                 '''\
Вас долго мучали инвентаризацией в кластере k8s, и по итогам вы нашли
никем не используемый под, потреблявший целую ноду. Опа, бесплатное железо!''',
                 '''\
В ЗИПе нашли лишнее железо, праздник на вашей улице!''']

    def __init__(self):
        super().__init__()
        self.short_text = 'Получаете '+self.component_name+' в ячейку %i'

    def apply(self, boards, num):
        board = boards[num]
        field = random.choice(board.all_nums_component(constants.EMPTY_CELL))
        board.change_component(self.component, field)
        return field


class AddRandomDBEvent(AddRandomAPIEvent):
    component = constants.DB
    component_name = 'DB'


class AddRandomLBEvent(AddRandomAPIEvent):
    component = constants.LB
    component_name = 'LB'


class DropCellEvent(BaseEvent):
    if constants.TEST: cards_count = 1 + 100
    short_text = 'Потеряна ячейка №%i'
    long_text = ['''\
ECC Memory Correctable Errors detected.
...
При замене планки ОЗУ браслет заземления случайно отстегнулся,
2U сервер был заочно приговорен к электрической казни.''',
                 '''\
Ваш сервер случайно уронили. Где в этот момент была стойка - умалчивается.''']

    def apply(self, boards, num):
        board = boards[num]
        num_cell = random.randint(1, constants.SIZE_BOARD**2)
        if board.is_admin and board.board[num_cell-1] == constants.DB:
            self.long_text = 'Ваш сервер случайно уронили. Но вы админ, моё почтение, снимаю шляпу!'
            self.short_text = 'Восстановлена ячейка №%i'
        else:
            board.del_component(num_cell)
        return num_cell


class BankruptEvent(BaseEvent):
    if constants.TEST: cards_count = 1 + 500
    short_text = 'Минус 1 очко на следующий ход.'
    long_text = ['''\
Бюджет вашего стартапа резко кончился, а инвесторов всё ещё не нашли,
требуется ужаться.''',
                 '''\
В середине года бюджет на год был успешно освоен, ждите новостей.''']

    def apply(self, boards, num):
        boards[num].bankrupt_points()
        return True


class AdminErrorEvent(BaseEvent):
    short_text = 'Коммутация вашех ячеек повернулась на 90°'
    long_text = ['''\
Ваши админы решили сэкономить на ЦОДе и прямо сейчас перевозят на тележке
последний сервер.
А теперь коммутируют его.
...
Ого, теперь БД из другой стойки отвечает быстрее на 1мс!
Ого, теперь она не в той стойке...
...
Зато остальные компоненты стали отвечать дольше на 1мс
...
Ноухау, горизонтальные стойки!''',
                 '''\
При переезде в другой ЦОД инженеры на объекте всё перепутали и разбросали
оборудование из одной стойки в разные.
...
Теперь говорят, что так лучше для охлаждения.''']

    def apply(self, boards, num):
        b = boards[num]
        new_b = [constants.EMPTY_CELL] * (constants.SIZE_BOARD**2)
        l_step = 0
        for ost in range(constants.SIZE_BOARD-1, 0-1, -1):
            for old_b_num in range(ost, constants.SIZE_BOARD**2, 4):
                new_b[l_step] = b.board[old_b_num]
                l_step += 1
        boards[num].board = new_b
        return True


class BonusEvent(BaseEvent):
    amount = 1
    penalty = 1
    short_text = "Пришло %iк, если не тянешь — потеря %iк"

    def apply(self, boards, num):
        # TODO: fix texts
        board = boards[num]
        b_cap = board.cap(board.quantity_component(constants.API),
                          board.quantity_component(constants.DB),
                          board.quantity_component(constants.LB))
        if b_cap < board.users+self.amount:
            board.change_users(-self.penalty)
        else:
            board.change_users(self.amount)
        return self.amount, self.penalty


class Bonus2Event(BonusEvent):
    amount = 2
    penalty = 1


class Bonus3Event(BonusEvent):
    amount = 3
    penalty = 1
    cards_count = 2


class DropComponentEvent(BaseEvent):
    if constants.TEST:  cards_count = 1 + 200
    short_text = "Компонент #%i потерян."

    def apply(self, boards, num):
        nums_comps = (boards[num].all_nums_component(constants.API) +
                      boards[num].all_nums_component(constants.DB) +
                      boards[num].all_nums_component(constants.LB) +
                      boards[num].all_nums_component(constants.BCKP))
        num_comp = random.choice(nums_comps)
        if boards[num].is_admin and boards[num].board[num_comp-1] == constants.DB:
            self.short_text = "Благодаря тому, что вы админ, компонент #%i не был потерян."
        else: boards[num].del_component(num_comp)
        return num_comp


class MoveComplonentToCompetitorEvent(BaseEvent):
    short_text = "По 1к пользователей ушли к конкуренту справа и слева"

    def apply(self, boards, num):
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
        return True


class DropRackEvent(BaseEvent):
    if constants.TEST:  cards_count = 2 + 100
    short_text = "Вылетела стойка #%i"
    long_text = ['''\
Наступила летняя жара, а зимой лишний кондиционер был не нужен и его продали.
Стойка, рядом с которой раньше стоял кондей, сгорела :(''',
                 '''\
Во время тестирования ИБП электрики что-то перепутали, и на одну из ваших
стоек пришла третья фаза вместо земли.
...
Помянем.''']

    def apply(self, boards, num):
        # фактически генерим номер стойки
        n = random.randint(1, 4)
        if boards[num].is_admin:
            self.long_text = 'Одна из ваших стоек начала барахлить, но вы, админ, очень грозно на неё посмотрели, и она заработала.'
            self.short_text = 'Вы не дали упасть стойке #%i'
        else:
            for i in range(n, constants.SIZE_BOARD**2+1, 4):
                boards[num].del_component(i)
        return n


class ComponentToRightCompetitorEvent(BaseEvent):
    short_text = "Компонент #%i ушел конкуренту справа."

    def apply(self, boards, num):
        nums_comps = (boards[num].all_nums_component(constants.API) +
                      boards[num].all_nums_component(constants.DB) +
                      boards[num].all_nums_component(constants.LB) +
                      boards[num].all_nums_component(constants.BCKP))
        num_comp = random.choice(nums_comps)
        comp = boards[num].board[num_comp-1]
        if boards[num].is_admin and comp == constants.DB:
            self.short_text = "Компонент #%i не ушел конкуренту справа, потому что вы его величество админ и ваши базы данных разбазариванию не подлежат ни при каких условиях."
        else:
            boards[num].del_component(num_comp)
            if num == len(boards)-1:
                num_new_board = 0
            else:
                num_new_board = num + 1
            num_new_comp = random.choice(
                boards[num_new_board].all_nums_component(constants.EMPTY_CELL))
            boards[num_new_board].change_component(comp, num_new_comp)
        return num_comp


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
        random_ev().act(boards, num, gui)
