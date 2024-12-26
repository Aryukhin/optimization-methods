import math

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
