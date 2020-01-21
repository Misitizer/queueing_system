import time
import math
import random
from itertools import accumulate

#random.seed(202908975465536587)

def newTimeInLin(Tzmin, Tzmax, u):
    return round((Tzmax - Tzmin) * u + Tzmin, 3)

def newTimeInExp(lam, u):
    return round(-(math.log(u) / lam), 3)

def newWorkTime(Tsmin, Tsmax, u):  # функция генерации времени обработки
    return round(((Tsmax - Tsmin) * u + Tsmin), 3)

def newWorkExp(Texp, u):
    mu = round(1/Texp, 3)
    return round(-(math.log(u) / mu), 3)

def generateTimes(Tzmin, Tzmax, Tsmin, Tsmax, lam, Texp, value, simTime):
    """ Генерирует времена для симуляции ВС. Генерирует время входов и времена обработки (время выходов)

    Tzmin -- минимальное время входа (default 0.333)
    Tzmax -- максимальное время входа (default 0.666)
    Tsmin -- минимальное время обработки программы (default 1)
    Tsmax -- максимальное время обрабоки программы (default 6)
    lam -- частота для экспоненциального закона (default 2)
    Texp -- среднее время обработки для экспоненциального закона (default 3)
    value -- флаг, который указывает на закон распределения (1 - линейное, 2 - экспоненциальное) (default 1)
    simTime -- время работы ВС. (default 3600)


    """


    # Времена прихода и выполнения заявок
    task_in_time = []
    task_in_int = []
    task_comp_time = []
    task_comp_int = []

    last_time = 0
    while round(sum(task_in_int), 3) < simTime:
        # Генерируем время прихода
        u = random.random()
        if value == 1:
            receive_time = newTimeInLin(Tzmin, Tzmax, u)
        elif value == 2:
            receive_time = newTimeInExp(lam, u)
        task_in_int.append(receive_time)
        last_time = round(sum(task_in_int), 3)


        # Генерируем время выполнения
        u = random.random()
        if value == 1:
            lead_time = newWorkTime(Tsmin, Tsmax, u)
        elif value == 2:
            lead_time = newWorkExp(Texp, u)
        task_comp_int.append(round(lead_time, 3))
        task_comp_time.append(round(last_time + lead_time, 3))
    task_in_time = [round(i,3) for i in list(accumulate(task_in_int))]

    return task_comp_int, task_comp_time, task_in_int, task_in_time

def simulate(Tzmin=0.333, Tzmax=0.666, Tsmin=1, Tsmax=6, simTime=3600, Texp=3, lam=2, value=1):
    """ Симулирует работу ВС. Является основной функцией (main) программы. Дефолтные значения из условия.

    Tzmin -- минимальное время входа (default 0.333)
    Tzmax -- максимальное время входа (default 0.666)
    Tsmin -- минимальное время обработки программы (default 1)
    Tsmax -- максимальное время обрабоки программы (default 6)
    simTime -- время работы ВС. (default 3600)
    Texp -- среднее время обработки для экспоненциального закона (default 3)
    lam -- частота для экспоненциального закона (default 2)
    value -- флаг, который указывает на закон распределения (1 - линейное, 2 - экспоненциальное) (default 1)


    """

    task_comp_int, task_comp_time, task_in_int, task_in_time = generateTimes(Tzmin, Tzmax, Tsmin, Tsmax, lam, Texp, value, simTime)
    times = []
    for input_time in task_in_time:
        times.append(input_time)
    for lead_time in task_comp_time:
        times.append(lead_time)
    # Каждое время внутри times отдельное событие, которое меняет состояние
    # ВС (записываем время входа и время выхода каждой программы)
    times = list(set(times))
    times = sorted(times)


    #Работаем ли мы или нет
    server_status = [0]

    # Обрабатываемая заявка сервера
    server_task = [0]

    # Время работы в простое, во время обработки программы, с одним буффером
    # двумя буферами и с тремя буферами.
    working_time = [0, 0, 0, 0, 0]

    # Буфер
    buffer = []

    # Всего заявок
    receivedNum = 0
    # Обработанные заявки
    completedNum = 0
    # Не обработанные заявки/заявки, которые выполянялись во время окончания работы ВС
    inprocessNum = 0
    cancelledNum = 0

    # Количество работающих серверов
    working_server = []

    # Количество программ в ВС
    average_task_count = []

    # Время нахождения программы в ВС
    average_timing = {}

    # Количество программ в буфере
    average_buf_count = []

    # Время нахождения программы в буфере
    average_buf_timing = {}

    # Текущие заявки в ВС
    curr_task = []

    # Время на котором мы заканчиваем
    last_time = 0

    # Время выполнения заявок из буфера
    buff_comp_time = []

    for curr_time in times:

        # Время между итерациями цикла
        passed_time = round(curr_time - last_time, 3)

        # Количество простаивающих серверов
        free_server = server_status.count(0)
        # Количество работающих серверов
        working_server.append(round((1 - free_server) * passed_time, 3))

        # Количество времени, когда работает сервер
        if free_server == 1:
            working_time[0] = round(working_time[0] + passed_time, 3)
        elif free_server == 0 and len(buffer) == 0:
            working_time[1] = round(working_time[1] + passed_time, 3)
        elif len(buffer) == 1:
            working_time[2] = round(working_time[2] + passed_time, 3)
        elif len(buffer) == 2:
            working_time[3] = round(working_time[3] + passed_time, 3)
        elif len(buffer) == 3:
            working_time[4] = round(working_time[4] + passed_time, 3)

        average_buf_count.append(round(len(buffer) * passed_time, 3))

        # Количество заявок в ВС в каждый момент времени
        average_task_count.append(round((inprocessNum + len(buffer)) * passed_time, 3))

        # Увеличиваем время нахождения выполняющихся заявок
        for current_task in curr_task:
            if current_task not in average_timing:
                average_timing[current_task] = 0
            average_timing[current_task] = round(average_timing[current_task] + passed_time, 3)

        for current_task in buffer:
            if current_task not in average_timing:
                average_timing[current_task] = 0
            if current_task not in average_buf_timing:
                average_buf_timing[current_task] = 0
            average_timing[current_task] = round(average_timing[current_task] + passed_time, 3)
            average_buf_timing[current_task] = round(average_buf_timing[current_task] + passed_time, 3)

        if curr_time > simTime:
            break

        if curr_time in task_in_time:
            # Увеличиваем счетчик пришедших заявок
            receivedNum += 1
            # Получаем индекс свободного сервера
            server_index = None
            #for index, server in enumerate(server_status):
            if server_status[0] == 0:
                server_index = 0

            # Есть свободный сервер
            if server_index is not None:
                # Изменяем статус сервера
                server_status[server_index] = task_comp_time[task_in_time.index(curr_time)]
                server_task[server_index] = curr_time
                # Увеличиваем счетчик выполняемых заявок
                inprocessNum += 1
                curr_task.append(curr_time)
            else:
                # Буфер не полон
                if len(buffer) != 3:
                    # Помещаем в буфер
                    buffer.append(curr_time)
                else:
                    # Увеличиваем счетчик невыполненных заявок
                    cancelledNum += 1

        if curr_time in task_comp_time or curr_time in buff_comp_time:
            # Определяем сервер выполнивший заявку
            #for index, server in enumerate(server_status):
            if server_status[0] == curr_time:
                curr_task.remove(server_task[0])
                # Изменяем статус сервера
                server_status[0] = 0
                server_task[0] = 0
                # Уменьшаем счетчик выполняемых заявок
                inprocessNum -= 1
                # Увеличиваем счетчик выполненных заявок
                completedNum += 1

            # Проверяем буфер
            for task in buffer:
                # Получаем индекс свободного сервера
                server_index = None
                #for index, server in enumerate(server_status):
                if server_status[0] == 0:
                    server_index = 0
                # Есть свободный сервер
                if server_index is not None:
                    # Изменяем состояние сервера
                    lead_time = round(curr_time + task_comp_int[task_in_time.index(task)], 3)
                    server_status[server_index] = lead_time
                    server_task[server_index] = task
                    # Заносим время конца выполнения в список
                    buff_comp_time.append(lead_time)
                    # Увеличиваем счетчик выполняемых заявок
                    inprocessNum += 1
                    # Удаляем из буфера
                    buffer.remove(task)
                    # Добавляем в выполняющиеся заявки
                    curr_task.append(task)
                    # добавляем новое время в times
                    if lead_time not in times:
                        times.append(lead_time)
                        times.sort()

        # Переопределяем последнее время
        last_time = curr_time
    probability = []
    for i in range(5):
        probability.append(round(working_time[i] / simTime, 6))

    Q = round((completedNum + inprocessNum) / receivedNum, 3)

    # Абсолютная пропускная способность
    S = round((completedNum + inprocessNum) / simTime, 3)

    # Вероятность отказа
    Pc = round(cancelledNum / receivedNum, 3)
    # Среднее число программ в ВС

    N_task = round(sum(average_task_count) / 3600, 3)

    N_buf = round(sum(average_buf_count) / 3600, 3)

    T_buf = round(N_buf / S, 3)

    T_task = round(T_buf + (1/Texp), 3)




    return probability, Q, S, Pc, N_task, T_task, N_buf, T_buf

