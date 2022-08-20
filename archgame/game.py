from archgame import cli
from archgame import constants
from archgame import events

def main(): #- общий план того что делает программа
    gui = cli.Cli()
    ev = events.Events()
    boards = gui.intro()
    winner = None
    num_sprint = 1
    while winner is None:
        gui.begin(num_sprint)
        gui.print_board(boards)

        for b in boards:
            add_u, add_c = gui.ask(b)
            # Возвращаем всем дефолтные очки на ход
            # Так как BankruptEvent устанавливает лимит на следующий спринт, это нужно делать здесь.
            b.default_points()
            for i in add_c:
                component, num = i
                b.change_component(component, num)
            b.users = min((add_u + b.users), b.cap(b.quantity_component(constants.API), b.quantity_component(constants.DB), b.quantity_component(constants.LB)))
        gui.print_board(boards)

        #разыграть рандомные события
        for num in range(len(boards)):
            try:
                ev.random_event(boards, num, gui)
            except Exception:
                print("Событие сломалось, для этого игрока ничего не происходит, играем дальше.")
            boards[num].class_benefit()

        #Наводим порядок
        #Проверка после эвента: тянет ли своих пользователей после действий ВСЕХ теперь его конструкция
        for num in range(len(boards)):
            boards[num].users = min(boards[num].users, boards[num].cap(boards[num].quantity_component(constants.API), boards[num].quantity_component(constants.DB), boards[num].quantity_component(constants.LB)))

        #Условие победы пока не определено, поставила первое попавшееся
        if num_sprint == constants.WIN_SCORE:
            max_users = -1
            winner = []
            for n in boards:
                if n.users >= max_users:
                    max_users = n.users
                    winner.append(n.name)
            gui.print_board(boards)
            gui.final(", ".join(winner))

        num_sprint += 1

if __name__ == "__main__":
    main()