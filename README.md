# Проект по методам оптимизации
Проект содержит несколько веток, в ветке парсера сейчас лежит вся актуальная работа над проектом
Этот проект содержит несколько основных файлов для парсинга и обработки данных.

## Структура проекта

### `data_parser.py`
Файл `data_parser.py` содержит основной код парсера, который отвечает за извлечение и обработку данных из файлов(работает вроде корректно сейчас).

### `utils.py`
Файл `utils.py` предназначен для оптимизации путей и других вспомогательных функций. **Внимание:** Этот файл пока не готов и находится в стадии разработки.

### `main.py`
Файл `main.py` является точкой входа в программу. Именно из этого файла происходит запуск и отладка всех остальных компонентов проекта.

## Как использовать

1. **Создайте директорию** на вашем компьютере, куда будет скопирован проект.
2. **Скопируйте репозиторий** с помощью команды:
   ```bash
   git clone <ссылка-на-репозиторий>
   cd <название-директории>
   ```
   возможно понадобится команда копирования всех веток, если скопируется только main
   ```bash
   git fetch --all
   ```
3.После внесения изменений в код, запушьте изменения в нужную ветку (feature/parcer):
   ```bash
   git checkout feature/parcer
   git add .
   git commit -m "Ваше сообщение о изменениях"
   git push origin feature/parcer
   ```
   
