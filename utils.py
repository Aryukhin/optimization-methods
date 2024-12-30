import os
import matplotlib.pyplot as plt
from math import pi
from data_parser import parse_input, parse_data_section, parse_route_section, parse_order_section
import math
from utils import *
from main_order import arc_len, check_elem_order, build_road, check_order, calculate_opt_route, cost_calculate
from Plot import *


def validate_order_against_data(order, data_blocks):
    """
    Проверяет, соответствуют ли блоки из ORDER данным из секции DATA.
    """
    block_usage = {}
    for block_name, _ in order:
        if block_name not in data_blocks:
            raise ValueError(f"Блок {block_name} из секции ORDER отсутствует в секции DATA.")
        block_usage[block_name] = block_usage.get(block_name, 0) + 1

    for block_name, used_quantity in block_usage.items():
        available_quantity = data_blocks[block_name]["quantity"]
        if used_quantity > available_quantity:
            raise ValueError(
                f"Блок {block_name} используется {used_quantity} раз, "
                f"что превышает доступное количество ({available_quantity}) в секции DATA."
            )


def build_route(order, data_blocks, start_point=(0, 0)):
    """
    Построение маршрута на основе секции ORDER.
    Проверяет, начинается и заканчивается ли маршрут в точке (0, 0).
    Возвращает список точек маршрута.
    """
    route_points = [start_point]
    current_point = start_point
    current_direction = (1, 0)  # Начальное направление: вправо

    for block_name, turn in order:
        # Определение направления движения
        if turn == 1:  # Направо
            current_direction = (current_direction[1], -current_direction[0])
        elif turn == -1:  # Налево
            current_direction = (-current_direction[1], current_direction[0])

        # Определение длины блока
        block_length = 1  # По умолчанию длина = 1
        if block_name.startswith("L") or block_name == "B1":
            block_length = int(block_name[1:])

        # Обновление координат в зависимости от длины блока
        for _ in range(block_length):
            current_point = (
                current_point[0] + current_direction[0],
                current_point[1] + current_direction[1],
            )
            route_points.append(current_point)

    # Проверка окончания маршрута
    if route_points[-1] != start_point:
        raise ValueError(
            f"Маршрут не заканчивается в точке {start_point}. "
            f"Конечная точка: {route_points[-1]}."
        )

    return route_points
def process_file(file_path):
    """
    Обрабатывает файл и возвращает разобранные секции данных.
    """
    print(f"Чтение файла: {file_path}")
    data_section, route_section, order_section = parse_input(file_path)

    print("Парсинг данных...")
    data_blocks = parse_data_section(data_section)
    route_points = parse_route_section(route_section)
    order_points = parse_order_section(order_section)

    print("Данные успешно обработаны.")
    return data_blocks, route_points, order_points


def calculate_route(data_blocks, route_points, order_points):
    """
    Рассчитывает маршрут и проверяет его корректность.
    """
    elems = {
        'L1': [1, 0], 'L2': [2, 0], 'L3': [3, 0], 'L4': [4, 0],
        'T4': [arc_len(3, pi / 4), pi / 4], 'T8': [arc_len(3, pi / 8), pi / 8],
        'B1': [4, 0]
    }

    if order_points:
        print("Проверка последовательности элементов...")
        check_elem_order(order_points, elems)

        print("Построение маршрута...")
        massiv, used_elems, sum_points = build_road(elems, order_points, [0, 0], route_points)
        check_order(massiv, route_points, used_elems, data_blocks)

        print("Расчёт стоимости маршрута...")
        cost = cost_calculate(used_elems, data_blocks, sum_points)
        print(f"Стоимость маршрута: {cost}")

        return massiv
    else:
        print("Маршрут не задан в секции ORDER. Попытка вычислить оптимальный маршрут...")
        order_points = calculate_opt_route(elems, data_blocks, route_points)
        return []  # Возвращаем пустой маршрут, если невозможно рассчитать.


# def plot_route(route_points):
#     """
#     Отрисовывает маршрут, используя matplotlib.
#     """
#     x_coords, y_coords = zip(*route_points)
#
#     plt.figure(figsize=(8, 8))
#     plt.plot(x_coords, y_coords, marker="o", linestyle="-", color="blue", label="Маршрут")
#     plt.scatter(0, 0, color="red", label="Начальная/конечная точка")
#     plt.title("Построенный маршрут")
#     plt.xlabel("X координата")
#     plt.ylabel("Y координата")
#     plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
#     plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
#     plt.grid(color="gray", linestyle="--", linewidth=0.5)
#     plt.legend()
#     plt.show()
#
#

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def find_optimal_route(route_points, data_blocks):
    if not route_points:
        raise ValueError("Секция ROUTE пуста.")
    if not data_blocks:
        raise ValueError("Секция DATA пуста.")

    total_cost = 0
    path = []
    current_position = (0, 0)  # Стартовая точка

    for i in range(1, len(route_points)):
        x1, y1 = current_position
        x2, y2, v = route_points[i]

        # Расстояние между текущей и следующей точкой
        d = distance(x1, y1, x2, y2)

        # Выбираем подходящий элемент дороги
        best_block = None
        best_cost = float('inf')

        for block, info in data_blocks.items():
            if info['quantity'] > 0:  # Доступен ли блок
                # Условие выбора блока
                block_cost = info['cost'] * math.ceil(d / info['length'])
                if block_cost < best_cost:
                    best_cost = block_cost
                    best_block = block

        if not best_block:
            raise ValueError("Не хватает блоков для построения маршрута.")

        # Уменьшаем доступное количество блоков
        data_blocks[best_block]['quantity'] -= 1

        # Добавляем блок в маршрут
        path.append(best_block)
        total_cost += best_cost + (v / (1 + d))  # Учитываем стоимость точки

        current_position = (x2, y2)

    return path, total_cost