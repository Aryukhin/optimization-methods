import os
import matplotlib.pyplot as plt
from math import pi
from data_parser import parse_input, parse_data_section, parse_route_section, parse_order_section
from utils import *
from main_order import arc_len, check_elem_order, build_road, check_order, calculate_opt_route, cost_calculate
from Plot import *

def main():
    file_path = 'LILA_9.txt'
    file_name = os.path.basename(file_path)

    try:
        # Парсинг данных
        print("Чтение данных из файла...")
        # Обработка файла
        data_blocks, route_points, order_points = process_file(file_path)
        print("Данные успешно считаны.")
        print("Секция DATA:", data_blocks)
        print("Секция ROUTE:", route_points)
        print("Секция ORDER:", order_points)
        print('----------------'*10)
        print(f'Рисуем спаршеные точки')
        plot_route_points(route_points)
        print('----------------'*10)

        if len(order_points) > 0:
            route_provided = True

        elems = {'L1': [1, 0], 'L2': [2, 0], 'L3': [3, 0], 'L4': [4, 0],
                 'T4': [arc_len(3, pi / 4), pi / 4], 'T8': [arc_len(3, pi / 8), pi / 8],
                 'B1': [4, 0]}
        print(f'Проверяем корректность данных')
        print('----------------'*10)
        if route_provided:
            check_elem_order(order_points, elems)
            massiv, used_elems, sum_points = build_road(elems, order_points, [0, 0], route_points)
            check_order(massiv, route_points, used_elems, data_blocks)
        else:
            print('Строим маршрут...')
            return 0
            order_points = calculate_opt_route(elems, data_blocks, route_points)
        print('----------------'*10)
        cost = cost_calculate(used_elems, data_blocks, sum_points)
        print(f"Стоимость дороги согласно секции ORDER составила: {cost}")
        print('----------------'*10)
        mas_x = [i[0] for i in massiv]
        mas_y = [i[1] for i in massiv]


        x_coords = [point[0] for point in route_points]
        y_coords = [point[1] for point in route_points]

        # Если маршрут рассчитан, отрисовываем его
        if massiv:
            plot_final_route(massiv, route_points, file_name)
        else:
            print("Не удалось построить маршрут.")
    except ValueError as e:
        print(f"Ошибка обработки файла: {e}")


if __name__ == "__main__":
    main()
