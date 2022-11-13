# -*-coding: utf-8 -*-
TEST = False
WIN_SCORE = 7  # До какого спринта играем
if TEST:
    WIN_SCORE = 4  # До какого спринта играем

# Очки
FIRST_SPRINT_POINTS = 4
LIM_POINTS = 2  # Очки на один ход
BANKRUPT_POINTS = LIM_POINTS // 2  # количество очков на ход при банкротстве

# Возможные классы игроков
ALL_CLASSES = ['A', 'M', 'P']

# Обозначения игровых элементов
API = "A"
DB = "D"
LB = "L"
BACKUP = "B"
EMPTY_CELL = " "
POSSIBLE_INPUTS = [API, DB, LB, BACKUP]

# Компоненты/сервисы
LIM_A = 3  # API может выдержать до 3к нагрузки
LIM_A_P = 5  # у прогеров - до 5к нагрузки
LIM_D = 3  # DB может поддерживать до 3х API
LIM_L = 3  # LB может обслуживать не больше 3х API
# В случае потери DB при возврате ее назад бэкап позволяет вернуть часть
# пользовательской базы, но не более стольких к.
LIM_B = 2

SIZE_BOARD = 4  # ширина и высота квадратного игрового поля

# Статусы для класса TelegaGamer
USER_INIT_ST = "init"
USER_WAIT_ST = "waiting"
USER_READY_ST = "ready"

# Статусы для класса TelegramGameServer
GAME_INIT_ST = "prepare"
GAME_START_ST = "started"
GAME_END_ST = "ended"
