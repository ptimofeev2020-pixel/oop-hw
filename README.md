# Домашнее задание: ООП — Интернет-магазин

Проект реализует классы для интернет-магазина с абстрактными базовыми классами,
миксинами, наследованием и валидацией.

## Структура проекта

```
├── data/
│   └── products.json
├── src/
│   ├── __init__.py
│   ├── classes.py            # BaseProduct, PrintMixin, Product, Smartphone,
│   │                         # LawnGrass, BaseCategory, Category, Order,
│   │                         # CategoryIterator
│   └── utils.py              # Загрузка данных из JSON
├── tests/
│   ├── __init__.py
│   ├── test_classes.py
│   └── test_utils.py
├── main.py
├── pyproject.toml
└── .flake8
```

## Реализованная функциональность

- Абстрактный класс BaseProduct (ABC) — родительский для Product
- Класс-миксин PrintMixin — печатает repr при создании объекта
- Product(PrintMixin, BaseProduct) — множественное наследование
- Smartphone и LawnGrass — наследники Product
- Абстрактный BaseCategory — общий для Category и Order
- Класс Order (доп. задание) — заказ с одним товаром, количеством и итогом
- Ограничения: __add__ через type(), add_product через isinstance()
- Приватные атрибуты, геттеры/сеттеры, __str__, __add__, CategoryIterator

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

- **Тесты:** 79 passed
- **Покрытие:** 95%
- **flake8:** OK
- **mypy:** OK (strict)
- **isort:** OK
