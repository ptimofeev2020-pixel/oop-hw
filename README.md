# Домашнее задание: ООП — Интернет-магазин

Проект реализует классы для интернет-магазина с обработкой исключений,
абстрактными классами, миксинами и наследованием.

## Структура проекта

```
├── data/
│   └── products.json
├── src/
│   ├── __init__.py
│   ├── classes.py            # BaseProduct, PrintMixin, Product, Smartphone,
│   │                         # LawnGrass, BaseCategory, Category, Order,
│   │                         # CategoryIterator, ZeroQuantityError
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_classes.py
│   └── test_utils.py
├── main.py
├── pyproject.toml
└── .flake8
```

## Реализованная функциональность

- ValueError при создании Product с quantity=0 ("Товар с нулевым количеством не может быть добавлен")
- Метод middle_price() в Category — средний ценник, обработка деления на ноль (возвращает 0)
- Пользовательское исключение ZeroQuantityError для add_product (try/except/else/finally)
- Абстрактные классы BaseProduct и BaseCategory, миксин PrintMixin
- Наследники Product: Smartphone, LawnGrass
- Класс Order, ограничения __add__ через type(), add_product через isinstance()

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

- **Тесты:** 61 passed
- **Покрытие:** 94%
- **flake8:** OK
- **mypy:** OK (strict)
- **isort:** OK
