# Домашнее задание: ООП — Интернет-магазин

Проект реализует классы для интернет-магазина: `Product` и `Category`
с приватными атрибутами, магическими методами, итератором и валидацией.

## Структура проекта

```
├── data/
│   └── products.json        # Данные о товарах
├── src/
│   ├── __init__.py
│   ├── classes.py            # Классы Product, Category, CategoryIterator
│   └── utils.py              # Загрузка данных из JSON
├── tests/
│   ├── __init__.py
│   ├── test_classes.py       # Тесты классов
│   └── test_utils.py         # Тесты утилит
├── main.py                   # Точка входа
├── pyproject.toml
└── .flake8
```

## Реализованная функциональность

- `Product.__str__()` — строковое представление: "Название, X руб. Остаток: X шт."
- `Category.__str__()` — "Название категории, количество продуктов: X шт." (сумма quantity)
- `Product.__add__()` — сложение: сумма (цена * количество) двух товаров
- `CategoryIterator` — итератор для перебора товаров категории в цикле for
- Приватные атрибуты `__products`, `__price` с геттерами/сеттерами
- Метод `add_product()`, класс-метод `new_product()`

## Установка

```bash
poetry install
```

## Запуск

```bash
python main.py
```

## Тестирование

```bash
pytest --cov=src --cov-report=term-missing
```

## Результаты

- **Тесты:** 75 passed
- **Покрытие:** 100%
- **flake8:** OK
- **mypy:** OK (strict)
- **isort:** OK
