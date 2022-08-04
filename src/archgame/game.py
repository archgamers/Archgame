from archgame import cli
from archgame import constants
from archgame import events
from archgame import texts


def main(): #- общий план того что делает программа
    gui = cli.Cli()
    boards = gui.intro()
    gui.first_sprint()

    winner = None
    num_sprint = 2
    while winner == None:
        gui.begin(boards, num_sprint)

        for b in boards:
            add_u, add_c = gui.ask(b)
            for i in add_c:
                component, num = i
                b.change_component(component, num)
            b.users = min((add_u + b.users), b.cap(b.quantity_component(texts.API), b.quantity_component(texts.DB), b.quantity_component(texts.LB)))
            gui.print_board(b)

        #ТЕСТ, потом уберу, как отлаживать всё окончу
        print("счет игроков:")
        for n in boards:
            print(n.name, n.users)

        #разыграть рандомные события
        for num in range(len(boards)):
            events.random_event(boards, num)
            #Проверка после эвента: тянет ли своих пользователей теперь его конструкция
            boards[num].users = min(boards[num].users, boards[num].cap(boards[num].quantity_component(texts.API), boards[num].quantity_component(texts.DB), boards[num].quantity_component(texts.LB)))

        #Условие победы пока не определено, поставила первое попавшееся
        if num_sprint == constants.WIN_SCORE:
            max_users = -1
            for n in boards:
                if n.users > max_users:
                    max_users = n.users
                    winner = n.name
            gui.final(winner)

        num_sprint += 1

if __name__ == "__main__":
    main()