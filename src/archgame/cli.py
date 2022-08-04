from archgame import texts
from archgame import obj
from archgame import constants

class Cli:
    def __int__(self):
        pass

    #НЕДОДЕЛКИ
    #Надо написать первый спринт, пока без него
    def first_sprint(self):
        # Выводить или не выводить легенду и когда вообще выводить - пока непонятно
        print(texts.LEGEND)
        pass

    #вывод поля
    def print_board(self, board):
        b = board.board
        s = []
        for i in range(len(b)+1):
            if (i > 0) and (i % constants.SIZE_BOARD == 0):
                print(s)
                s = []
                if i == len(b): break
            s += [b[i]]
        print("Player:", board.name)
        print("Users:", board.users)
        print("Cap:",board.cap(board.quantity_component(texts.API), board.quantity_component(texts.DB), board.quantity_component(texts.LB)))
        # #cli
        # # Оригинал для вдохновения код написать
        # """
        # Света      Саша       Гера
        # |A| | | |  |A| | | |  |A| | | |
        # | |D| | |  | |D| | |  | |D| | |
        # | | |B| |  | | |B| |  | | |B| |
        # | | | | |  | | | | |  | | | | |
        # Users: 1   Users: 1   Users: 1
        # Cap: 3     Cap: 3     Cap: 3
        # """
        #
        # def cli(self):
        #     # 9 символов на столбец, 2 пробела между столбцами
        #     s1 = ""
        #     for i in range(len(Board.names)):
        #         s1 += Board.names[i] + " " * (9 - len(Board.names[i]))
        #     print(s1)
        #     s2



    def intro(self):
        q_hero = int(input(texts.ASK_QUANTITY))
        boards = [0] * q_hero
        for i in range(1, q_hero+1, 1):
            name = input(texts.ASK_NAME % i).strip()
            boards[i-1] = obj.Board(name)
            boards[i-1].default()
        return(boards)

    def begin(self, boards, num_sprint):
        print(texts.SPRINTS % num_sprint)
        print(texts.DESC)

    #вернет массив вида 1) скольк надо добавить u  2) [[компонент, номер ячейки], [...]...]
    def ask(self, b):
        # Посчитала нормальным каждому игроку показывать его поле отдельно перед ходом, так удобнее ему выбирать действие
        self.print_board(b)
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
