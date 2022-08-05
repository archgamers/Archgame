WIN_SCORE = 7 # До какого спринта играем
LIM_POINTS = 2 # Очки на один ход

#Обозначения игровых элементов
API = "A"
DB = "D"
LB = "L"
BCKP = "B"
EMPTY_CELL = " "
POSSIBLE_INPUTS = [API, DB, LB, BCKP]

#Компоненты/сервисы
LIM_A = 3 # API может выдержать до 3к нагрузки
LIM_D = 3 # DB может поддерживать до 3х API
LIM_L = 3 # LB может обслуживать не больше 3х API
LIM_B = 2 # В случае потери DB при возврате ее назад бэкап позволяет вернуть часть пользовательской базы, но не более стольких к.

SIZE_BOARD = 4 # ширина и высота квадратного игрового поля

#Вероятности событий, event's chance
CHANCE_DBA = 3
CHANCE_DEL_API = 1
CHANCE_BANKRUPT = 1
CHANCE_ADD_RANDOM_API = 1
CHANCE_ADD_RANDOM_DB = 1
CHANCE_ADD_RANDOM_LB = 1
CHANCE_DROP_CELL = 1
CHANCE_ADMIN_ERROR = 1
CHANCE_ADD_1K = 1
CHANCE_ADD_2K = 1
CHANCE_ADD_3K = 2
CHANCE_DROP_COMPONENT = 1
CHANCE_LEFT_RIGHT_1K = 1
CHANCE_DROP_RACK = 2
CHANCE_RIGHT_COMPONENT = 1

#Флаг банкротства
BANKRUPT = False
BANKRUPT_NAME = ""
BANKRUPT_POINTS = LIM_POINTS//2