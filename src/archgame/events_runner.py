from archgame import cli
from archgame import constants
from archgame import events
from archgame import texts

gui = cli.Cli()
ev = events.Events()
boards = gui.intro()
gui.first_sprint()

num_sprint = 1
while num_sprint <= constants.WIN_SCORE:
    print("Спринт %d" % num_sprint)
    # разыграть рандомные события
    for num in range(len(boards)):
        ev.random_event(boards, num, gui)
        boards[num].default()
    input("Игроки, время действовать!")

    num_sprint += 1