import matplotlib.pyplot as plt
import seaborn as sns

def plot_route_points(route):
    """
    Построение графика точек маршрута из секции ROUTE.

    Args:
        route (list of tuples): Список точек в формате (x, y, v), где:
                                x, y - координаты точки,
                                v - стоимость точки.
    """
    # Разделяем координаты x, y и значения v
    x_coords = [point[0] for point in route]
    y_coords = [point[1] for point in route]
    v_values = [point[2] for point in route]

    # Построение графика
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(x_coords, y_coords, c=v_values, cmap='viridis', s=100, edgecolor='black')
    plt.colorbar(scatter, label='v (стоимость точки)')

    # Подписи осей и заголовок
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.title('График точек маршрута (ROUTE) с их стоимостью (v)')

    # Отображение сетки
    plt.grid(True)

    # Показ графика
    plt.show()

def plot_final_route(massiv, route_points, file_name):
    """
    Построение итогового маршрута с точки из секции ROUTE.

    Args:
        massiv (list of tuples): Итоговый маршрут в формате (x, y).
        route_points (list of tuples): Точки из секции ROUTE.
        file_name (str): Имя анализируемого файла.
    """
    # Разделяем координаты для маршрута
    mas_x = [point[0] for point in massiv]
    mas_y = [point[1] for point in massiv]

    # Разделяем координаты для точек ROUTE
    x_coords = [point[0] for point in route_points]
    y_coords = [point[1] for point in route_points]

    # Построение графика
    plt.figure(figsize=(10, 8))
    plt.plot(mas_x, mas_y, 'r-', linewidth=2, label='Маршрут', alpha=0.8)
    plt.scatter(x_coords, y_coords, c='blue', edgecolor='black', s=100, label='Точки маршрута (ROUTE)', zorder=3)

    # Подписи осей и заголовок
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.title(f'Итоговый маршрут (файл: {file_name})')

    # Легенда и сетка
    plt.legend(loc='upper left', fontsize=10, frameon=True, shadow=True, fancybox=True, borderpad=1)
    plt.grid(True)

    # Показ графика
    plt.show()
