import matplotlib.pyplot as plt


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

    # # Добавление номеров точек
    # for idx, (x, y, v) in enumerate(route):
    #     plt.text(x, y, str(idx), fontsize=9, color='red', ha='right')

    # Подписи осей и заголовок
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.title('График точек маршрута (ROUTE) с их стоимостью (v)')

    # Отображение сетки
    plt.grid(True)

    # Показ графика
    plt.show()
