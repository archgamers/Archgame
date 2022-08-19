import sys
import time

from archgame import texts
from archgame import obj
from archgame import constants


class InvalidUserInput(Exception):
    pass


input_speed = {
    '\n': 0.5,
}


class Cli:
    def __int__(self):
        pass

    def cli_print(self, texts):
        if constants.TEST:
            input(texts)
            return()
        for line in texts:
            print('')
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(input_speed.get(char, 0.03))
        input('')


    #вывод поля
    def print_board(self, boards):
        lines = [""] * 7
        for b in boards:
            lines[0] += b.name + " " + b.class_per + " " * (11-len(b.name) - 1 - len(b.class_per))
            s = []
            for i in range(len(b.board) + 1):
                if (i > 0) and (i % constants.SIZE_BOARD == 0):
                    lines[i//constants.SIZE_BOARD] += ("|" + "|".join(s) + "|  ")
                    s = []
                    if i == len(b.board): break
                s += [b.board[i]]
            line_u = "Users:" + str(b.users)
            lines[5] += line_u + " " * (11-len(line_u))
            line_c = "Cap:" + str(b.cap(b.quantity_component(constants.API), b.quantity_component(constants.DB), b.quantity_component(constants.LB)))
            lines[6] += line_c + " " * (11-len(line_c))
        for l in lines: print(l)

    def intro(self):
        q_hero = int(input(texts.ASK_QUANTITY))
        print(texts.ASK_CLASSES)
        boards = [0] * q_hero
        for i in range(1, q_hero+1, 1):
            name, cl = input(texts.ASK_NAME % i).strip().split(",")
            boards[i-1] = obj.Player(name.strip(), cl.strip())
        print(texts.LEGEND)
        return boards

    def begin(self, num_sprint):
        print('\n\n\n')
        print(texts.SPRINTS % num_sprint)
        if num_sprint == 1:
            print(texts.DESC % constants.FIRST_SPRINT_POINTS)
        else:
            print(texts.DESC % constants.LIM_POINTS)

    @staticmethod
    def validate_input_user(choices, b):
        if len(choices) != b.q_point:
            raise InvalidUserInput
        for choice in choices:
            if '-' in choice:
                input_list = choice.split('-')
                if len(input_list) != 3:
                    raise InvalidUserInput
                _, component, num_cell = choice.split('-')
                if num_cell.isdigit() == False:
                    raise InvalidUserInput
                num_cell = int(num_cell)
                if component not in constants.POSSIBLE_INPUTS:
                    raise InvalidUserInput
                if 0 > num_cell or num_cell > constants.SIZE_BOARD ** 2 + 1:
                    raise InvalidUserInput

            elif choice != '1':
                raise InvalidUserInput

    # вернет массив вида 1) скольк надо добавить u  2) [[компонент, номер ячейки], [...]...]
    def ask(self, b):
        while True:
            try:
                inpt_str = input(texts.INPUT_ACTION % b.name).strip()
                choices = inpt_str.split(',')
                self.validate_input_user(choices, b)
                ans = [0, []]
                for i in choices:
                    if i[0] == "1":  # добавить юзеров
                        ans[0] += 1
                    if i[0] == "2":  # добавить компонент
                        two, comp, number = i.strip().split("-")
                        ans[1].append([comp, int(number)])
                return ans
            except InvalidUserInput:
                print('Некорректный ввод, пожалуйста, попробуйте снова,\nПомните, что на ход вам даётся %d очка' % b.q_point)



    def final(self, winner):
        print(texts.ENDING % winner)
