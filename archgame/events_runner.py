from archgame import cli
from archgame import constants
from archgame import events

gui = cli.Cli()
ev = events.Events()
boards = gui.intro()

num_sprint = 1
while num_sprint <= constants.WIN_SCORE:
    print("Спринт %d" % num_sprint)
    # разыграть рандомные события
    for num in range(len(boards)):
        ev.random_event(boards, num, gui)
        boards[num].default()
    input("\nИгроки, время действовать!\n")

    num_sprint += 1