from archgame import texts
from archgame import obj
from archgame import constants

class Cli:
    def __int__(self):
        pass

    def cli_print(self, texts):
        print(" ".join(texts))

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
            line_c = "Cap:" + str(b.cap(b.quantity_component(texts.API), b.quantity_component(texts.DB), b.quantity_component(texts.LB)))
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
        print(texts.SPRINTS % num_sprint)
        print(texts.DESC)

    #вернет массив вида 1) скольк надо добавить u  2) [[компонент, номер ячейки], [...]...]
    def ask(self, b):
        inpt_str = input(texts.INPUT_ACTION % b.name).strip().split(",")
        ans = [0, []]
        for i in inpt_str:
            if i[0] == "1": #добавить юзеров
                ans[0] += 1
            if i[0] == "2": # добавить компонент
                two, comp, number = i.strip().split("-")
                ans[1].append([comp, int(number)])
        return(ans)

    def final(self, winner):
        print(texts.ENDING % winner)