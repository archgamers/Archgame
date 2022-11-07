# -*-coding: utf-8 -*-
import sys
import time
import telebot

from archgame import texts
from archgame import constants

input_speed = {
    '\n': 0.5,
}


class Cli:
    def __init__(self, slow_print):
        self.slow_print = slow_print

    def ask(self, name):
        return input(texts.INPUT_ACTION % name).strip()

    def output_input_msg(self, text):
        if not self.slow_print:
            print("".join(text))
            input('')
            return
        for line in text:
            print('')
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(input_speed.get(char, 0.03))
        input('')

    def output_print_msg(self, text):
        if not self.slow_print:
            print("".join(text))
            return
        for line in text:
            print('')
            for char in line:
                sys.stdout.write(char)
                sys.stdout.flush()
                time.sleep(input_speed.get(char, 0.03))

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

    # Сделала 2 одинаковые по функционалу метода, чтобы не переписывать
    # уже написанный код.
    def output_input_msg(self, text):
        self.bot.send_message(self.chat_id, text)

    def output_print_msg(self, text):
        self.bot.send_message(self.chat_id, text)

    def ask(self, name):
         pass  # придумать схему состояний...

    # buttons - словарь вида
    # {"callbackdata": "что должно быть написано на кнопке"}
    def create_keyboard(self, message_text, buttons):
        keyboard = telebot.types.InlineKeyboardMarkup()
        for current_callbackdata in buttons:
            key_1 = telebot.types.InlineKeyboardButton(
                text=buttons[current_callbackdata],
                callback_data=current_callbackdata)
            keyboard.add(key_1)  # добавляем кнопку в клавиатуру
        self.bot.send_message(self.chat_id, text=message_text,
                              reply_markup=keyboard)
