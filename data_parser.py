import re

def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_section, route_section, order_section = [], [], []
    current_section = None

    for line in lines:
        line = line.split('--')[0].strip()  # Удаляем комментарии
        if not line:
            continue

        if line == "DATA":
            current_section = data_section
        elif line == "ROUTE":
            current_section = route_section
        elif line == "ORDER":
            current_section = order_section
        elif line == "/":
            current_section = None
        elif current_section is not None:
            current_section.append(line)

    return data_section, route_section, order_section


def parse_data_section(data_section):
    data_blocks = {}
    for item in data_section:
        parts = re.split(r'\s+', item)  # Разделяем строку по пробелам
        if len(parts) != 3:
            raise ValueError(f"Некорректная строка в секции DATA: '{item}'")

        block_type = parts[0]  # Тип блока (например, L1, T4)
        try:
            quantity = int(parts[1])  # Количество
            cost = int(parts[2])  # Стоимость
        except ValueError as e:
            raise ValueError(f"Ошибка при преобразовании данных: {e} в строке '{item}'")

        data_blocks[block_type] = {
            "quantity": quantity,
            "cost": cost,
            #"length": int(block_type.split('_')[-1]) if "_" in block_type else 0
            # Извлечение длины блока (если применимо)
        }
    return data_blocks


def parse_route_section(route_section):
    route_points = []
    for item in route_section:
        parts = re.split(r'\s+', item)
        if len(parts) != 3:
            raise ValueError(f"Некорректная строка в секции ROUTE: '{item}'")
        x, y, v = map(int, parts)
        route_points.append((x, y, v))
    return route_points

def parse_order_section(order_section):
    order = []
    for item in order_section:
        parts = re.split(r'\s+', item)
        if len(parts) != 2:
            raise ValueError(f"Некорректная строка в секции ORDER: '{item}'")
        block_type, direction = parts
        order.append((block_type, int(direction)))
    return order