# -*-coding: utf-8 -*-

import logging
from logging import config as logging_config
from optparse import OptionParser
import os.path
import random
import sys
import telebot
import uuid

from archgame import game_server
from archgame import gamers
from archgame import texts
from archgame import cli
from archgame import constants


RULES_CMD = 'rules'
TRIAL_CMD = 'trial'
NEW_CMD = 'new'
RUN_CMD = 'run'
JOIN_CMD = 'join'
RESET_CMD = 'reset'
STATUS_CMD = 'status'
DEFAULT_USER_NAME = 'Anon'

DEFAULT_CONFIG = {
    'version': 1,
    'formatters': {
        'aardvark': {
            'datefmt': '%Y-%m-%d,%H:%M:%S',
            'format': "%(asctime)15s.%(msecs)03d %(processName)s"
                      " pid:%(process)d tid:%(thread)d %(levelname)s"
                      " %(name)s:%(lineno)d %(message)s"
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'aardvark',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        'archgame': {},
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
}


def log_init():
    logging_config.dictConfig(DEFAULT_CONFIG)


def parse_cli():
    parser = OptionParser()

    # # Available actions
    parser.add_option("--token-file", "-t", dest="token_file", type="string",
                      default="./token.txt",
                      help="Path to telegram token file. Default is %default")

    options, _ = parser.parse_args()
    if not os.path.isfile(options.token_file):
        print("Not found file with token. Exiting.")
        sys.exit(1)

    with open(options.token_file) as tfile:
        token = tfile.read().strip()

    return options, token


def _get_random_class():
    return random.choice(constants.ALL_CLASSES)


def _validate_user_class_input(class_text):
    # Class - Admin
    if class_text in ['A', 'a', 'А', 'а']:
        return 'A'
    # Class - Programmer
    elif class_text in ['P', 'p', 'П', 'п', 'Р', 'р']:
        return 'P'
    # Class - Manager
    elif class_text in ['M', 'm', 'М', 'м']:
        return 'M'
    else:
        return _get_random_class()


def _parse_username_class(text, cmd=TRIAL_CMD):
    text = text.strip()
    if cmd:
        text = text.replace('/' + cmd, '')
    splitted_text = text.strip().split()
    if splitted_text:
        user_name = splitted_text[0]
    else:
        user_name = DEFAULT_USER_NAME
    if len(splitted_text) > 1:
        user_class = _validate_user_class_input(splitted_text[1])
    else:
        user_class = _get_random_class()
    return user_name, user_class


class GameStorage:
    def __init__(self, log):
        self.players = {}
        self.games = {}
        self.log = log

    def has_player(self, user_id):
        return user_id in self.players

    def player_status_is(self, user_id, status):
        if not self.has_player(user_id):
            return False
        if isinstance(status, set):
            return self.get_player(user_id).status in status
        return self.get_player(user_id).status == status

    def has_game(self, game_uuid):
        return game_uuid in self.games

    def get_player(self, user_id):
        if self.has_player(user_id):
            return self.players[user_id]
        return None

    def get_game(self, game_uuid):
        if self.has_game(game_uuid):
            return self.games[game_uuid]
        return None

    def game_started_for_player(self, user_id,
                                started_game_statuses=constants.GAME_STARTED):
        return (self.has_player(user_id) and
                self.has_game(self.get_player(user_id).game_uuid) and
                self.get_game(self.get_player(user_id).game_uuid).status in
                started_game_statuses)

    def get_game_for_user(self, user_id):
        user = self.get_player(user_id)
        return self.get_game(user.game_uuid)

    def create_game(self, game_owner=None):
        # For more safety convert uuid to str
        game_uuid = str(uuid.uuid4())
        self.games[game_uuid] = game_server.TelegramGameServer(
            game_uuid, game_owner=game_owner)
        self.log.info('Create game %s', game_uuid)
        return game_uuid

    def create_player(self, user_name, user_id, game_uuid, user_class, bot):
        io = cli.TelegramIO(bot=bot, chat_id=user_id)
        self.players[user_id] = gamers.TelegaGamer(name=user_name,
                                                   user_id=user_id,
                                                   game_uuid=game_uuid,
                                                   class_per=user_class,
                                                   g_cli=io)
        self.log.info('Create player %s with id %s',
                      self.players[user_id], user_id)
        return self.players[user_id]

    def add_player_to_game(self, game_uuid, player):
        self.games[game_uuid].add_gamer(player)

    def start_game(self, game_uuid):
        self.games[game_uuid].start_game()

    def delete_game(self, game_uuid):
        if not self.has_game(game_uuid):
            return
        self.games.pop(game_uuid)
        self.log.info('Delete game %s', game_uuid)

    def delete_player(self, user_id):
        if not self.has_player(user_id):
            return
        self.players.pop(user_id)
        self.log.info('Delete player %s', user_id)

    def force_delete_game(self, game_uuid):
        # Remove game and all players
        for player in self.get_game(game_uuid).gamers:
            self.delete_player(player.user_id)
        self.delete_game(game_uuid)

    def del_game_on_end(self, game_uuid):
        if not self.has_game(game_uuid):
            return
        if self.get_game(game_uuid).status == constants.GAME_END_ST:
            self.force_delete_game(game_uuid)


def out_user_name_class(cid, name, user_class, bot=None):
    class_hum = texts.CLASSES_USER_READABLE[user_class]
    bot.send_message(cid, texts.TELEGRAM_USER_INFO % (name, class_hum))


def run_trial_game(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Get command %s for chat %s', TRIAL_CMD, cid)

    if storage.game_started_for_player(cid):
        bot.send_message(cid, texts.TELEGRAM_GAME_ALREADY_STARTED)
        log.debug('User %s already in game, but want trial game', cid)
        return

    user_name, user_class = _parse_username_class(message.text)
    out_user_name_class(cid, user_name, user_class, bot)
    log.info('Run trial game for user "%s" with name "%s" and class "%s"',
             cid, user_name, user_class)

    # Create game and player
    game_uuid = storage.create_game(game_owner=cid)
    player = storage.create_player(user_name, cid, game_uuid, user_class, bot)
    storage.add_player_to_game(game_uuid, player)

    # Create bots for game
    bot_classes = set(constants.ALL_CLASSES) - set(user_class)
    for num, bot_class in enumerate(bot_classes):
        bot_player = gamers.TelegaBot(num, bot_class)
        log.debug('Add bot %s to game %s', bot_player, game_uuid)
        storage.add_player_to_game(game_uuid, bot_player)

    # Run game
    try:
        storage.start_game(game_uuid)
    except Exception as err:
        log.exception("Error in game start for user %s and game %s: %s", cid,
                      game_uuid, str(err))


def create_new_game(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Get command %s for chat %s', NEW_CMD, cid)

    if storage.game_started_for_player(cid):
        bot.send_message(cid, texts.TELEGRAM_GAME_ALREADY_STARTED)
        log.debug('User %s already in game, but want new game', cid)
        return

    user_name, user_class = _parse_username_class(message.text, cmd=NEW_CMD)
    out_user_name_class(cid, user_name, user_class, bot)
    log.info('Run new game for user "%s" with name "%s" and class "%s"',
             cid, user_name, user_class)

    game_uuid = storage.create_game(game_owner=cid)
    player = storage.create_player(user_name, cid, game_uuid, user_class, bot)
    storage.add_player_to_game(game_uuid, player)

    # Inform user about created game
    bot.send_message(cid, texts.TELEGRAM_GAME_CREATED)
    bot.send_message(cid, game_uuid)

    # Switch game_server to waiting status
    # Game in this status is considered running
    storage.get_game(game_uuid).set_status(constants.GAME_WAIT_ST)


def run_created_game(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Get command %s for chat %s', RUN_CMD, cid)

    if storage.game_started_for_player(cid):
        game = storage.get_game_for_user(cid)
        if game.game_owner == cid and game.status == constants.GAME_WAIT_ST:
            try:
                storage.start_game(game.game_uuid)
            except Exception as err:
                log.exception(
                    "Error in game start for user %s and game %s: %s",
                    cid, game.game_uuid, str(err)
                )
        else:
            log.debug('User %s want to run not owned game', cid)
            bot.send_message(cid, texts.TELEGRAM_START_FORBIDEN)
    else:
        bot.send_message(cid, texts.TELEGRAM_GAME_NOT_STARTED)
        log.debug('User %s want to run game, but game not found', cid)


def join_in_game(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Get command %s for chat %s', JOIN_CMD, cid)

    if storage.game_started_for_player(cid):
        bot.send_message(cid, texts.TELEGRAM_GAME_ALREADY_STARTED)
        log.debug(
            'User %s already in game, but want join to another game', cid)
        return

    user_name, user_class = _parse_username_class(message.text, cmd=JOIN_CMD)
    out_user_name_class(cid, user_name, user_class, bot)
    log.info('Join to game user "%s" with name "%s" and class "%s"',
             cid, user_name, user_class)

    # Create player without game
    player = storage.create_player(user_name, cid, None, user_class, bot)
    # Swith player to join status
    player.set_status(constants.USER_JOIN_ST)
    bot.send_message(cid, texts.TELEGRAM_JOIN_INFO)


def join_input_game(message, log, bot, storage):
    cid = message.chat.id
    game_uuid = message.text
    log.debug('User %s trying join game %s', cid, game_uuid)
    if (storage.has_game(game_uuid) and
            storage.get_game(game_uuid).status == constants.GAME_WAIT_ST):
        # Add player to game
        player = storage.get_player(cid)
        storage.add_player_to_game(game_uuid, player)
        # Reset the user state to the original for the normal operation of the
        # /reset and /status command
        player.set_status(constants.USER_INIT_ST)
        bot.send_message(cid, texts.TELEGRAM_GAME_STARTED_STATUS % game_uuid)
    else:
        log.debug('Game %s for user %s not found. Games avail: %s',
                  game_uuid, cid, storage.games.keys())
        bot.send_message(cid, texts.TELEGRAM_JOIN_GAME_FAIL % game_uuid)
        bot.send_message(cid, texts.TELEGRAM_JOIN_INFO)


def check_user_status(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Get command %s for chat %s', STATUS_CMD, cid)
    if storage.game_started_for_player(cid):
        game = storage.get_game_for_user(cid)
        bot.send_message(cid, texts.TELEGRAM_GAME_STARTED_STATUS %
                         game.game_uuid)
        bot.send_message(cid, texts.TELEGRAM_STATUS_PLAYERS_INTRO)
        # Show info about another players
        for player in game.gamers:
            status = texts.TELEGRAM_USER_STATUS_HUMAN_READABLE[player.status]
            user_class = texts.CLASSES_USER_READABLE[player.class_per]
            bot.send_message(cid, texts.TELEGRAM_STATUS_PLAYER_INFO %
                             (player.name, user_class, status))
    elif storage.player_status_is(cid, constants.USER_JOIN_ST):
        bot.send_message(cid, texts.TELEGRAM_JOIN_INFO)
    else:
        bot.send_message(cid, texts.TELEGRAM_GAME_IDLE_STATUS)


def reset_user(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Get command %s for chat %s', RESET_CMD, cid)

    if storage.player_status_is(cid, constants.USER_JOIN_ST):
        log.debug('Get reset for joining player %s', cid)
        storage.delete_player(storage.get_player(cid).user_id)
        bot.send_message(cid, texts.TELEGRAM_JOIN_GAME_RESET)
        return

    if not storage.game_started_for_player(cid):
        bot.send_message(cid, texts.TELEGRAM_GAME_IDLE_STATUS)
        return

    game = storage.get_game_for_user(cid)
    if game.game_owner == cid:
        log.info('Reset game %s for all', game.game_uuid)
        storage.force_delete_game(game.game_uuid)
        bot.send_message(
            cid, texts.TELEGRAM_GAME_RESET_SUCCESS % game.game_uuid)
    else:
        # TODO: Allow the user to exit someone else's game
        bot.send_message(cid, texts.TELEGRAM_GAME_NOT_OWNER % game.game_uuid)


def handling_ingame_input(message, log, bot, storage):
    cid = message.chat.id
    log.debug('Check input for user %s', cid)
    if storage.game_started_for_player(cid):
        user = storage.get_player(cid)
        game = storage.get_game_for_user(cid)
        try:
            user.set_user_input(message.text)
            game.check_sprint_next_step()
            storage.del_game_on_end(game.game_uuid)
        except Exception as err:
            log.exception("Error in game step for user %s and game %s: %s",
                          cid, game.game_uuid, str(err))


def main():
    # opts, token = parse_cli()
    opts, token = ["", "5717283892:AAGwLHlDu5-gYAA00W6FsyZiajJtx2VlpTU"]
    log_init()
    log = logging.getLogger(__name__)
    storage = GameStorage(log=log)

    try:
        bot = telebot.TeleBot(token)
    except Exception as err:
        log.exception('Fail to init connection to Telegram API: %s', err)
        sys.exit(1)

    @bot.message_handler(commands=['start', 'help'])
    def start_handler(message, res=False):
        log.debug('Send help to chat "%s"', message.chat.id)
        bot.send_message(message.chat.id, texts.TELEGRAM_HELP)

    @bot.message_handler(commands=[RULES_CMD])
    def rules_handler(message, res=False):
        log.debug('Send rules to chat "%s"', message.chat.id)
        bot.send_message(message.chat.id, texts.TELEGRAM_RULES)

    @bot.message_handler(commands=[TRIAL_CMD])
    def trial_handler(message, res=False):
        run_trial_game(message, log, bot, storage)

    @bot.message_handler(commands=[STATUS_CMD])
    def status_handler(message, res=False):
        check_user_status(message, log, bot, storage)

    @bot.message_handler(commands=[NEW_CMD])
    def new_handler(message, res=False):
        create_new_game(message, log, bot, storage)

    @bot.message_handler(commands=[RUN_CMD])
    def run_handler(message, res=False):
        run_created_game(message, log, bot, storage)

    @bot.message_handler(commands=[RESET_CMD])
    def reset_handler(message, res=False):
        reset_user(message, log, bot, storage)

    @bot.message_handler(commands=[JOIN_CMD])
    def join_handler(message, res=False):
        join_in_game(message, log, bot, storage)

    @bot.message_handler(
        func=lambda msg:
            storage.player_status_is(msg.chat.id, constants.USER_JOIN_ST))
    def user_join_handler(message):
        join_input_game(message, log, bot, storage)

    @bot.message_handler(
        func=lambda msg:
            storage.player_status_is(msg.chat.id, constants.USER_WAIT_ST))
    def user_ingame_handler(message):
        handling_ingame_input(message, log, bot, storage)

    log.info('Start Telegram API polling')
    # Restart on error and not reset storage
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as err:
            log.exception('Error connection to Telegram API: %s', err)


if __name__ == "__main__":
    main()
