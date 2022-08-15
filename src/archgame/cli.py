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
        for line in texts:
            print('')
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(input_speed.get(char, 0.03))
        input('')

    #НЕДОДЕЛКИ
    #Надо написать первый спринт, пока без него
    def first_sprint(self):
        # Выводить или не выводить легенду и когда вообще выводить - пока непонятно
        print(texts.LEGEND)
        pass


    #вывод поля
    def print_board(self, boards):
        lines = [""] * 7
        for b in boards:
            lines[0] += b.name + " " * (11-len(b.name))
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
        boards = [0] * q_hero
        for i in range(1, q_hero+1, 1):
            name = input(texts.ASK_NAME % i).strip()
            boards[i-1] = obj.Board(name)
            boards[i-1].default()
        return boards

    def begin(self, boards, num_sprint):
        print('\n\n\n')
        print(texts.SPRINTS % num_sprint)
        print(texts.DESC)

    # #вернет массив вида 1) скольк надо добавить u  2) [[компонент, номер ячейки], [...]...]
    # def ask(self, b):
    #     inpt_str = input(texts.INPUT_ACTION % b.name).strip().split(",")
    #     ans = [0, []]
    #     for i in inpt_str:
    #         if i[0] == "1": #добавить юзеров
    #             ans[0] += 1
    #         if i[0] == "2": # добавить компонент
    #             two, comp, number = i.strip().split("-")
    #             ans[1].append([comp, int(number)])
    #     return(ans)
    @staticmethod
    def validate_input_user(choices, lim_points):
        if len(choices) > lim_points:
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

    def ask(self, b, default=constants.LIM_POINTS):
        while True:
            try:
                inpt_str = input(texts.INPUT_ACTION % b.name).strip()
                choices = inpt_str.split(',')
                self.validate_input_user(choices, default)
                ans = [0, []]
                for i in choices:
                    if i[0] == "1":  # добавить юзеров
                        ans[0] += 1
                    if i[0] == "2":  # добавить компонент
                        two, comp, number = i.strip().split("-")
                        ans[1].append([comp, int(number)])
                return ans
            except InvalidUserInput:
                print('Некорректный ввод, пожалуйста, попробуйте снова,\nПомните, что на ход вам даётся %d очка' % default)



    def final(self, winner):
        print(texts.ENDING % winner)
