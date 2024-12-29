from data_parser import *
from utils import find_optimal_route

def main():
    file_path = 'LILA/LILA_1.txt'  # Убедитесь, что путь к файлу правильный

    try:
        # Парсинг данных
        print("Чтение данных из файла...")
        data_section, route_section, order_section = parse_input(file_path)

        print("Данные успешно считаны.")
        print("Секция DATA:", data_section)
        print("Секция ROUTE:", route_section)
        print("Секция ORDER:", order_section)

        print("Парсинг секции DATA...")
        data_blocks = parse_data_section(data_section)
        print("Секция DATA разобрана:", data_blocks)

        print("Парсинг секции ROUTE...")
        route_points = parse_route_section(route_section)
        print("Секция ROUTE разобрана:", route_points)

        print("Парсинг секции ORDER...")
        order_points = parse_order_section(order_section)
        print("Секция ORDER разобрана:", order_section)

        # Нахождение оптимального маршрута
        # print("Нахождение оптимального маршрута...")
        # optimal_path, minimal_cost = find_optimal_route(route_points, data_blocks)

        # Вывод результатов
        print("Оптимальный маршрут:")
        for i, block in enumerate(optimal_path, 1):
            print(f"{i}. {block}")
        print(f"Минимальная стоимость маршрута: {minimal_cost}")

    except FileNotFoundError as fnf_error:
        print(f"Ошибка: файл не найден: {fnf_error}")
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
