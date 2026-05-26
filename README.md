# Домашнее задание: ООП — Интернет-магазин

Проект реализует классы для интернет-магазина с наследованием,
магическими методами, валидацией и ограничениями типов.

## Структура проекта

```
├── data/
│   └── products.json        # Данные о товарах
├── src/
│   ├── __init__.py
│   ├── classes.py            # Product, Smartphone, LawnGrass, Category, CategoryIterator
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

- Наследники Product: Smartphone (efficiency, model, memory, color) и LawnGrass (country, germination_period, color)
- Ограничение __add__: сложение только товаров одного типа (через type()), иначе TypeError
- Ограничение add_product: принимает только Product или наследников (isinstance), иначе TypeError
- __str__ для Product и Category, __add__ для Product
- Приватные атрибуты __products, __price с геттерами/сеттерами
- Класс-метод new_product(), итератор CategoryIterator

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

- **Тесты:** 89 passed
- **Покрытие:** 100%
- **flake8:** OK
- **mypy:** OK (strict)
- **isort:** OK
