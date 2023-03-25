from archgame import constants
import random

import csv
import inspect
import sys


# Во все события передавать всё одинаково!
# Когда буду делать отображение надписей для событий - передавать во все
# объект Cli ещё!!!


class BaseEvent(object):
    short_text = ''
    physical_game_short_text = ''
    long_text = ''
    immunity_text = ''
    cards_count = 1

    @property
    def random_long_text(self):
        if isinstance(self.long_text, list):
            return random.choice(self.long_text)
        return self.long_text

    def apply(self, gamers, num):
        # If applied - return True or tuple which will be formatted into
        #   output string.
        raise NotImplementedError()

    def act(self, gamers, num, output_func=None):
        result = self.apply(gamers, num)
        response = [gamers[num].name + ":", self.random_long_text, '\n\n']
        if result is None:
            response.append(self.immunity_text)
        else:
            response.append(self.short_text % result
                            if result is not True else self.short_text)
        if output_func:
            output_func(response)
        else:
            gamers[num].input_message(response)


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

    def apply(self, gamers, num):
        if gamers[num].is_admin:
            self.long_text = '''\
Ваш аутсорсер-DBA переносил реплики и почти удалил таблицу,
но вы вовремя дали ему по шапке и успешно сделали всё сами.'''
            self.short_text = '''Данные спасены.'''
            self.immunity_text = ''
            pass
        else:
            if gamers[num].is_a_component(constants.BACKUP):
                gamers[num].del_component(
                    random.choice(
                        gamers[num].all_nums_component(constants.BACKUP)))
                return None
            else:
                gamers[num].users = 0
                return True


class DelApiEvent(BaseEvent):
    short_text = 'API #%i потеряна.'
    long_text = ['''\
Вам повезло, хабра-эффект принёс много клиентов!
...
Но одна из API не выдержала и взорвалась :(''',
                 '''\
На сервере кончились inodes, но никто этого не заметил
...
Зато после обновления одна из ваших API не запустилась''',
                 ]
    cards_count = 2

    def apply(self, gamers, num):
        num_rand_comp = random.choice(
            gamers[num].all_nums_component(constants.API))
        gamers[num].del_component(num_rand_comp)
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
один из их сервисов :)''',
                 ]

    def __init__(self):
        super().__init__()
        self.short_text = 'Получаете ' + self.component_name + ' в ячейку #%i'

    def apply(self, gamers, num):
        field = random.choice(
            gamers[num].all_nums_component(constants.EMPTY_CELL))
        gamers[num].change_component(self.component, field)
        return field


class AddRandomDBEvent(AddRandomAPIEvent):
    component = constants.DB
    component_name = 'DB'
    long_text = ['''\
Вас долго мучали инвентаризацией в кластере k8s, и по итогам вы нашли
никем не используемый под, потреблявший целую ноду. Опа, бесплатное железо!''',
                 ]


class AddRandomLBEvent(AddRandomAPIEvent):
    component = constants.LB
    component_name = 'LB'
    long_text = ['''\
В ЗИПе нашли лишнее железо, праздник на вашей улице!'''
                 ]


class DropCellEvent(BaseEvent):
    # if constants.TEST:
    #     cards_count = 1 + 100
    short_text = 'Потеряна ячейка #%i'
    long_text = ['''\
ECC Memory Correctable Errors detected.
...
При замене планки ОЗУ браслет заземления случайно отстегнулся,
2U сервер был заочно приговорен к электрической казни.''',
                 '''\
Ваш сервер случайно уронили. Где в этот момент была стойка - умалчивается.''',
                 '''\
ххх: Слушай, сервак больше не отвечает
yyy: И не будет, он разобранный лежит на моем столе!
xxx: Ну и какого...? Предупреждать надо!
yyy: Я предупреждал... Ты почту когда последний раз читал?''',
                 ]
    cards_count = 3

    def apply(self, gamers, num):
        num_cell = random.randint(1, constants.SIZE_BOARD ** 2)
        if gamers[num].is_admin \
                and (num_cell in gamers[num].all_nums_component(constants.DB)):
            self.long_text = '''\
Ваш сервер случайно уронили. Но вы админ, моё почтение, снимаю шляпу!'''
            self.short_text = 'Восстановлена ячейка #%i'
        else:
            gamers[num].del_component(num_cell)
        return num_cell


class BankruptEvent(BaseEvent):
    # if constants.TEST:
    #     cards_count = 1 + 500
    short_text = 'Минус 1 очко на следующий ход.'
    long_text = ['''\
Бюджет вашего стартапа резко кончился, а инвесторов всё ещё не нашли,
топ менеджмент требуется ужаться.''',
                 '''\
В середине года бюджет на год был успешно освоен, ждите новостей.''']
    cards_count = 2

    def apply(self, gamers, num):
        gamers[num].bankrupt_points()
        return True


class AdminErrorEvent(BaseEvent):
    short_text = 'Коммутация ваших ячеек повернулась на 90°'
    long_text = ['''\
Ваши админы решили сэкономить на ЦОДе и прямо сейчас перевозят на тележке
последний сервер.
А теперь коммутируют его.
...
Ого, теперь БД из другой стойки отвечает быстрее на 1мс!
Ого, теперь она не в той стойке...
...
Зато остальные сервисы стали отвечать дольше на 1мс
...
Ноухау, горизонтальные стойки!''',
                 '''\
При переезде в другой ЦОД инженеры на объекте всё перепутали и разбросали
оборудование из одной стойки в разные.
...
Теперь говорят, что так лучше для охлаждения.''']
    cards_count = 2

    def apply(self, gamers, num):
        new_b = [constants.EMPTY_CELL] * (constants.SIZE_BOARD ** 2)
        l_step = 0
        for ost in range(constants.SIZE_BOARD - 1, 0 - 1, -1):
            for old_b_num in range(ost, constants.SIZE_BOARD ** 2, 4):
                new_b[l_step] = gamers[num].return_comp(old_b_num)
                l_step += 1
        gamers[num].board.board = new_b
        return True


class BonusEvent(BaseEvent):
    amount = 1
    penalty = 1
    short_text = "Пришло %i юзеров, если не тянешь — теряешь %i юзеров"
    long_text = ['''\
Ваш маркетинг высадил весь бюджет на рекламу, радуйтесь потоку пользователей!

Но вам о рекламе не сказали, посмотрим, насколько готова наша инфра к DDoS.''',
                 '''\
О, реклама наконец заработала!

Откуда так много клиентов?!?! 0_0''']
    cards_count = 2

    def __init__(self):
        super().__init__()
        self.physical_game_short_text = (
            "Пришло %i юзеров, если не тянешь — "
            "теряешь %i юзеров" % (self.amount, self.penalty))

    def apply(self, gamers, num):
        # TODO: fix texts
        b_cap = gamers[num].cap(gamers[num].quantity_component(constants.API),
                                gamers[num].quantity_component(constants.DB),
                                gamers[num].quantity_component(constants.LB))
        if b_cap < gamers[num].users + self.amount:
            gamers[num].change_users(-self.penalty)
        else:
            gamers[num].change_users(self.amount)
        return self.amount, self.penalty


class Bonus2Event(BonusEvent):
    amount = 2
    penalty = 1
    cards_count = 2


class Bonus3Event(BonusEvent):
    amount = 3
    penalty = 2
    cards_count = 2


class DropComponentEvent(BaseEvent):
    # if constants.TEST:
    #     cards_count = 1 + 200
    short_text = "Сервис #%i потерян."
    long_text = ['''\
Пришел oom-killer, в следующий раз пишите код лучше :-)''',
                 '''\
Опа, Segmentation fault...''',
                 ]
    cards_count = 2

    def apply(self, gamers, num):
        nums_comps = (gamers[num].all_nums_component(constants.API) +
                      gamers[num].all_nums_component(constants.DB) +
                      gamers[num].all_nums_component(constants.LB) +
                      gamers[num].all_nums_component(constants.BACKUP))
        num_comp = random.choice(nums_comps)
        if gamers[num].is_admin \
                and (num_comp in gamers[num].all_nums_component(constants.DB)):
            self.short_text = ("Благодаря тому, что вы админ, компонент #%i "
                               "не был потерян.")
        else:
            gamers[num].del_component(num_comp)
        return num_comp


class MoveComplonentToCompetitorEvent(BaseEvent):
    cards_count = 2
    short_text = "По 1к пользователей ушли к конкуренту справа и слева"
    long_text = '''\
xxx: Гляди какое дело... Вижу по графикам, что нагрузка уменьшилась
xxx: Но не понимаю - с чего бы... Можешь у NOC выяснить?
yyy: Хм, NOC'и говорят что продали префикс в котором мы использовали адрес
yyy: А в DNS мы поменять забыли...
yyy: Теперь наши пользователи обслуживаются кем-то... Но не нами ((('''

    def apply(self, gamers, num):
        if gamers[num].users >= 2:
            if num == len(gamers) - 1:
                gamers[0].change_users(1)
                gamers[num - 1].change_users(1)
            elif num == 0:
                gamers[len(gamers) - 1].change_users(1)
                gamers[num + 1].change_users(1)
            else:
                gamers[num - 1].change_users(1)
                gamers[num + 1].change_users(1)
        else:
            if gamers[num].users == 0:
                self.short_text = "Конкурентам не повезло, пользователей нет."
            if gamers[num].users == 1:
                self.short_text = "Пользователь ушел конкуренту справа"
                gamers[num].change_users(-1)
                if num == len(gamers) - 1:
                    gamers[0].change_users(1)
                else:
                    gamers[num + 1].change_users(1)
        gamers[num].change_users(-2)
        return True


class DropRackEvent(BaseEvent):
    # if constants.TEST:
    #     cards_count = 2 + 100
    short_text = "Вылетела стойка #%i"
    long_text = ['''\
Наступила летняя жара, а зимой лишний кондиционер был не нужен и его продали.
Стойка, рядом с которой раньше стоял кондей, сгорела :(''',
                 '''\
Во время тестирования ИБП электрики что-то перепутали, и на одну из ваших
стоек пришла третья фаза вместо земли.
...
Помянем.''']
    cards_count = 2

    def apply(self, gamers, num):
        # фактически генерим номер стойки
        n = random.randint(1, 4)
        if gamers[num].is_admin:
            self.long_text = (
                'Одна из ваших стоек начала барахлить, но вы, '
                'админ, очень грозно на неё посмотрели, и она заработала.')
            self.short_text = 'Вы не дали упасть стойке #%i'
        else:
            for i in range(n, constants.SIZE_BOARD ** 2 + 1, 4):
                gamers[num].del_component(i)
        return n


class ComponentToRightCompetitorEvent(BaseEvent):
    short_text = "Сервис #%i ушел конкуренту справа."
    long_text = """\
ххх: Слушай, ты же дежурный админ?
ххх: По моему сервису сработал canary check... Глянешь?
yyy: Сча...
yyy: Слушай, тут такое дело...
yyy: Кажется мы перепутали и задеплоили ваш сервис...
yyy: Куда-то не туда..."""

    def apply(self, gamers, num):
        nums_comps = (gamers[num].all_nums_component(constants.API) +
                      gamers[num].all_nums_component(constants.DB) +
                      gamers[num].all_nums_component(constants.LB) +
                      gamers[num].all_nums_component(constants.BACKUP))
        num_comp = random.choice(nums_comps)
        comp = gamers[num].return_comp(num_comp - 1)
        if gamers[num].is_admin and comp == constants.DB:
            self.short_text = """\
Компонент #%i не ушел конкуренту справа, потому что вы его величество админ и
ваши базы данных разбазариванию не подлежат ни при каких условиях."""
        else:
            gamers[num].del_component(num_comp)
            if num == len(gamers) - 1:
                num_new_board = 0
            else:
                num_new_board = num + 1
            num_new_comp = random.choice(
                gamers[num_new_board].all_nums_component(constants.EMPTY_CELL))
            gamers[num_new_board].change_component(comp, num_new_comp)
        return num_comp


clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
game_events = [event[1] for event in clsmembers if issubclass(event[1],
                                                              BaseEvent)
               and event[1] is not BaseEvent]


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

    def random_event(self, gamers, num, ouput_func=None):
        try:
            random_ev = self.events.pop()
        except IndexError:
            self.events = self.refill_events()
            random_ev = self.events.pop()
        random_ev().act(gamers, num, output_func=ouput_func)


def generate_events_list():
    texts = []

    for ev in game_events:
        ev = ev()
        for num in range(ev.cards_count):
            if ev.physical_game_short_text:
                short_text = ev.physical_game_short_text
            else:
                short_text = ev.short_text
            if isinstance(ev.long_text, str):
                long_text = ev.long_text
            else:
                if len(ev.long_text) < num:
                    long_text = ev.long_text[-1]
                else:
                    long_text = ev.long_text[num]
            texts.append((long_text, short_text))

    if len(sys.argv) > 1 and sys.argv[1] == 'shuffle':
        random.shuffle(texts)

    csvwriter = csv.writer(sys.stdout)
    for row in texts:
        csvwriter.writerow(row)


def check_events():
    import inspect
    template = "::warning file="+__file__+",line=%i::"
    errors = 0
    for ev in game_events:
        ev = ev()
        if isinstance(ev.long_text, str):
            continue
        if len(ev.long_text) != ev.cards_count:
            print(template % inspect.findsource(ev.__class__)[1] +
                  'Event texts count doesn\'t match with cards number: %s' %
                  ev.__class__.__name__)
            errors += 1

    print(errors)
    if errors:
        return errors
