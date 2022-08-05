from archgame import cli
from archgame import constants
from archgame import events
from archgame import texts


def main(): #- общий план того что делает программа
    gui = cli.Cli()
    ev = events.Events()
    boards = gui.intro()
    gui.first_sprint()

    #Тест!
    # import sys
    # num_sprint = 1
    # while num_sprint <= constants.WIN_SCORE:
    #     print("Спринт %d" % num_sprint)
    #     # разыграть рандомные события
    #     for num in range(len(boards)):
    #         ev.random_event(boards, num, gui)
    #         boards[num].default()
    #         input()
    #     num_sprint += 1
    # sys.exit(0)
    # Тест!

    winner = None
    num_sprint = 2
    while winner == None:
        gui.begin(boards, num_sprint)
        gui.print_board(boards)

        for b in boards:
            if constants.BANKRUPT and constants.BANKRUPT_NAME == b.name:
                add_u, add_c = gui.ask(b, default=(constants.BANKRUPT_POINTS))
                constants.BANKRUPT = False
            else:
                add_u, add_c = gui.ask(b)
            for i in add_c:
                component, num = i
                b.change_component(component, num)
            b.users = min((add_u + b.users), b.cap(b.quantity_component(constants.API), b.quantity_component(constants.DB), b.quantity_component(constants.LB)))
        gui.print_board(boards)

        #разыграть рандомные события
        for num in range(len(boards)):
            ev.random_event(boards, num, gui)

        #Проверка после эвента: тянет ли своих пользователей после действий ВСЕХ теперь его конструкция
        for num in range(len(boards)):
            boards[num].users = min(boards[num].users, boards[num].cap(boards[num].quantity_component(constants.API), boards[num].quantity_component(constants.DB), boards[num].quantity_component(constants.LB)))

        #Условие победы пока не определено, поставила первое попавшееся
        if num_sprint == constants.WIN_SCORE:
            max_users = -1
            for n in boards:
                if n.users > max_users:
                    max_users = n.users
                    winner = n.name
            gui.print_board(boards)
            gui.final(winner)

        num_sprint += 1

if __name__ == "__main__":
    main()