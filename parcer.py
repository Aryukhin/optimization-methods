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
        parts = re.split(r'\s+', item)
        if len(parts) == 3:
            block_type, quantity, cost = parts
            data_blocks[block_type] = {
                "quantity": int(quantity),
                "cost": int(cost)
            }
    return data_blocks

def parse_route_section(route_section):
    route_points = []
    for item in route_section:
        parts = re.split(r'\s+', item)
        if len(parts) == 3:
            x, y, v = map(int, parts)
            route_points.append((x, y, v))
    return route_points

def parse_order_section(order_section):
    order = []
    for item in order_section:
        parts = re.split(r'\s+', item)
        if len(parts) == 2:
            block_type, direction = parts
            order.append((block_type, int(direction)))
    return order

# Основной код для тестирования парсера
file_path = 'D:\Загрузки\LILA_9.txt'  # Укажите путь к входному файлу

data_section, route_section, order_section = parse_input(file_path)

# Парсинг секций
data_blocks = parse_data_section(data_section)
route_points = parse_route_section(route_section)
order = parse_order_section(order_section)

# Вывод результатов для проверки
print("DATA Section:")
print(data_blocks)

print("ROUTE Section:")
print(route_points)

print("ORDER Section:")
print(order)
