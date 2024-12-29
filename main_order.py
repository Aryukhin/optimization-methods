from data_parser import *
from math import cos, pi, sin, sqrt
import matplotlib.pyplot as plt
import os
import argparse

def build_road(elems, order, start_point, route_points):
    ans = True
    elems_dict = {}
    point_array = [start_point]
    nu = 0
    x, y = start_point
    sum_points = 0
    i = 0
    for item in order:
        if item[0] in elems:
            length, alpha = elems[item[0]]
            elems_dict[item[0]] = elems_dict.get(item[0], 0) +  1
            if alpha != 0:
                if item[1] < 0:
                    alpha *= item[1]
                else:
                    alpha *= 1
                ab = sqrt(18 - 12*cos(alpha))
            else:
                ab = length
            x, y = x + ab*sin(alpha), y + ab*cos(alpha)
            if nu == 0:
                point_array.append([round(x, 3), round(y, 3)])
            else:
                temp_x, temp_y = x*cos(2*pi - nu) - y*sin(2*pi - nu), x*sin(2*pi - nu) + y*cos(2*pi - nu)
                point_array.append([round(temp_x, 3), round(temp_y, 3)])

            for item in route_points:
                if point_array[-1][0] == item[0] and point_array[-1][1] == item[1]:
                    v = item[-1]
                    if i < len(order) - 1:
                        d = min(elems[order[i][0]][0], elems[order[i+1][0]][0])
                    else:
                        d = elems[order[i][0]][0]
                    sum_points += v/(1 + d)

            nu += alpha
            x, y = x*cos(alpha) - y*sin(alpha), x*sin(alpha) + y*cos(alpha)
            i += 1

    return point_array, elems_dict, sum_points

def check_elem_order(order, elems):
    ans = True
    for item in order:
        if item[0] not in elems:
            print(f"  В последовательности используется несуществующий элемент")
            ans = False
        if item[1] not in [1, -1]:
            print(f"  Некорректное направление движения: элемент - {item[0]}: {item[1]}")
            ans = False
    return ans

def check_order(point_array, route_points, used_elems, data):
    ans = True
    for item in route_points:
        if [item[0], item[1]] not in point_array:
            print(f"  Маршрут не проходит через обязательную точку: ({item[0]}, {item[1]})")
            ans = False
    if point_array[0] != [0, 0]:
        print(f"  Маршрут начинается не в точке (0, 0)")
        ans = False
    if point_array[-1] != [0, 0]:
        print(f"  Маршрут заканчивается не в точке (0, 0)")
        ans = False
    for item in used_elems.items():
        if item[1] > data[item[0]]['quantity']:
            print(f"  Недостаточное количество строительных элементов: {item[0]} = {item[1]} больше, чем указано в DATA: {data[item[0]]['quantity']}")
            ans = False
    return ans

def cost_calculate(used_elems, data, sum_points):
    sum_elems = 0
    for item in used_elems.items():
        sum_elems += data[item[0]]['cost']*used_elems[item[0]]
    return sum_points - sum_elems

def arc_len(radius, alpha):
    return pi*radius/180*alpha

def calculate_opt_route(elems, data_section, route_points):
    opt_points = []
    routed_points = []
    point_num = 1
    for x, y, weight in route_points:
        if x == 0 and y == 0:
            continue
        if weight <= 0:
            continue
        else:
            opt_points.append({
                'num': point_num,
                'x': x,
                'y': y,
                'weight': weight
            })
            point_num += 1

        # Здесь может быть сортировка массива точек.


    # print("Оптимальные точки маршрута:")
    # for point in opt_points:
    #     print(f'  {point["num"]}: ({point["x"]}, {point["y"]})')


def main():
    route_provided = False

    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, help='Полный путь к файлу')
    args = parser.parse_args()

    file_path = args.file_path
    print(f"Переданный путь: {file_path}")

    file_name = os.path.basename(file_path)
    print(f'Анализ файла `{file_name}`:')

    data_section, route_section, order_section = parse_input(file_path)
    data_blocks = parse_data_section(data_section)
    route_points = parse_route_section(route_section)
    order_points = parse_order_section(order_section)

    if len(order_points) > 0:
        route_provided = True

    elems = {'L1':[1, 0], 'L2':[2, 0], 'L3':[3, 0], 'L4':[4, 0],
             'T4':[arc_len(3, pi/4), pi/4], 'T8':[arc_len(3, pi/8), pi/8],
             'B1':[4, 0] }

    if route_provided:
        check_elem_order(order_points, elems)
        massiv, used_elems, sum_points = build_road(elems, order_points, [0, 0], route_points)
        check_order(massiv, route_points, used_elems, data_blocks)
    else:
        print('Строим маршрут...')
        return 0
        order_points = calculate_opt_route(elems, data_blocks, route_points)

    cost = cost_calculate(used_elems, data_blocks, sum_points)
    print(f"Стоимость дороги согласно секции ORDER составила: {cost}")

    mas_x = [i[0] for i in massiv]
    mas_y = [i[1] for i in massiv]

    plt.figure()
    plt.plot(mas_x, mas_y, 'r-', label='Маршрут')

    x_coords = [point[0] for point in route_points]
    y_coords = [point[1] for point in route_points]

    plt.plot(x_coords, y_coords, 'b.', label='Точки маршрута из секции ROUTE')

    plt.xlabel('X координата')
    plt.ylabel('Y координата')

    plt.title(f'Результат анализа файла {file_name}')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

    plt.subplots_adjust(left=0.2, right=0.6)

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()