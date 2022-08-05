WIN_SCORE = 5 # До какого спринта играем

#Компоненты/сервисы
LIM_A = 3 # API может выдержать до 3к нагрузки
LIM_D = 3 # DB может поддерживать до 3х API
LIM_L = 3 # LB может обслуживать не больше 3х API
LIM_B = 2 # В случае потери DB при возврате ее назад бэкап позволяет вернуть часть пользовательской базы, но не более стольких к.

SIZE_BOARD = 4 # ширина и высота квадратного игрового поля

#Вероятности событий, event's chance
CHANCE_DBA = 0
CHANCE_DEL_API = 0
CHANCE_BANKRUPT = 0
CHANCE_ADD_RANDOM_API = 0
CHANCE_ADD_RANDOM_DB = 0
CHANCE_ADD_RANDOM_LB = 0
CHANCE_DROP_CELL = 0
CHANCE_ADMIN_ERROR = 1
CHANCE_ADD_1K = 0
CHANCE_ADD_2K = 0
CHANCE_ADD_3K = 0
CHANCE_DROP_COMPONENT = 1
CHANCE_LEFT_RIGHT_1K = 1
CHANCE_DROP_RACK = 1
CHANCE_RIGHT_COMPONENT = 1