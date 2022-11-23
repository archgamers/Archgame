# -*-coding: utf-8 -*-
import sys
import time

from archgame import texts
from archgame import constants
from telebot import formatting

input_speed = {
    '\n': 0.01,
}


class Cli:
    def __init__(self, slow_print):
        self.slow_print = slow_print

    def _pretty_print(self, text):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(input_speed.get(char, 0.001))
        print('')

    def ask(self, name):
        return input(texts.INPUT_ACTION % name).strip()

    def output_input_msg(self, text):
        if not self.slow_print:
            print("".join(text))
            input('')
            return
        print('')
        if isinstance(text, list):
            for line in text:
                self._pretty_print(line)
        else:
            self._pretty_print(text)
        input('')

    def output_print_msg(self, text):
        if not self.slow_print:
            print("".join(text))
            return
        if isinstance(text, list):
            for line in text:
                self._pretty_print(line)
        else:
            self._pretty_print(text)

    def print_board(self, board, name, class_per, users, cap):
        lines = [""] * 7
        lines[0] += name + " " + class_per + " " * (constants.SIZE_BOARD * 2
                                                    + 3 - len(name) - 1 -
                                                    len(class_per))
        s = []
        for i in range(constants.SIZE_BOARD**2 + 1):
            if (i > 0) and (i % constants.SIZE_BOARD == 0):
                lines[i //
                      constants.SIZE_BOARD] += ("|" +
                                                "|".join(s) +
                                                "|  ")
                s = []
                if i == constants.SIZE_BOARD**2:
                    break
            s += [board.board[i]]
        line_u = "Users:" + str(users)
        lines[5] += line_u + " " * (constants.SIZE_BOARD * 2 + 3 -
                                    len(line_u))
        line_c = "Cap:" + str(cap)
        lines[6] += line_c + " " * (constants.SIZE_BOARD * 2 + 3 -
                                    len(line_c))
        return lines


class BotIO(Cli):
    def output_input_msg(self, text):
        super(BotIO, self).output_print_msg(text)


class EmptyIO(Cli):
    def output_input_msg(self, text):
        pass

    def output_print_msg(self, text):
        pass

    def print_board(self, board, name, class_per, users, cap):
        return []

    def statistic(self, statistics):
        for c in statistics:
            print(
                "Class:{0} Count:{1} Users:{2}/{3}/{4} Cap:{5}/{6}/{7}".format(
                    c, statistics[c][0],
                    statistics[c][1][0],
                    statistics[c][1][1],
                    statistics[c][1][2],
                    statistics[c][2][0],
                    statistics[c][2][1],
                    statistics[c][2][2]))


class TelegramIO(Cli):
    def __init__(self, bot, chat_id):
        super(TelegramIO, self).__init__(False)
        self.slow_print = False
        self.bot = bot
        self.chat_id = chat_id

    def output_input_msg(self, text):
        if not self.slow_print:
            self.bot.send_message(self.chat_id,
                                  formatting.format_text("".join(text)),
                                  parse_mode='HTML')
            return

        for line in text:
            self.bot.send_message(self.chat_id, line)

    def output_print_msg(self, text):
        self.output_input_msg(text)
