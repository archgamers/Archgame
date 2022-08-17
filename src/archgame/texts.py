from archgame import constants

ASK_QUANTITY = "Сколько будет игроков? "
ASK_CLASSES = """Классы игроков:
М - менеджер, невероятно обаятелен, каждый ход к нему просто так приходит 1 user
Р - программист, властелин-АПИ, у него они держат больше остальных - целых 5 users каждая
А - админ, неустрашим - в его кармане всегда есть флешка с продом, бэкап встроенный, не падает БД ни при каких обстоятельствах """
ASK_NAME = "Введите имя и класс игрока(через запятую) %d "

LEGEND = """A - API: умеет принимать нагрузку от пользователей, может выдержать до {0}к
    нагрузки, для работы нужна DB

D - DB: умеет обрабатывать запросы от API, может поддерживать до {1}х API

L - LoadBalancer: Позволяет масштабировать API, без него максимальная
    производительность всех API не превышает производительности одного API. Может
    обслуживать не больше {2}х API

B - Backup: В случае ошибки DBA позволяет избежать потери пользовательской
    базы, но снимается с игрового поля.
""".format(constants.LIM_A, constants.LIM_D, constants.LIM_L)

SPRINTS = "Спринт %d:"

INPUT_ACTION = "Введите действие для игрока %s: "

DESC = """
Вам пришло финансирование, у каждого игрока есть 2 очка, которые он может
потратить либо на привлечение новых пользователей(1), либо на установку новых
сервисов(2):
"""

ENDING = "Поздравляем победителя %s!!!"
