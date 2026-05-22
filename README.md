# Домашнее задание: ООП — Интернет-магазин

Проект реализует классы для интернет-магазина: `Product` и `Category`
с приватными атрибутами, геттерами/сеттерами, класс-методами и валидацией.

## Структура проекта

```
├── data/
│   └── products.json        # Данные о товарах
├── src/
│   ├── __init__.py
│   ├── classes.py            # Классы Product и Category
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

- Приватный атрибут `__products` в `Category` с геттером `products` (формат строки)
- Метод `add_product()` для добавления товаров
- Класс-метод `Product.new_product()` для создания из словаря (с проверкой дубликатов)
- Приватный атрибут `__price` в `Product` с геттером и сеттером (валидация + подтверждение понижения)

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

## Линтеры

```bash
flake8 src tests main.py
mypy src main.py
isort --check src tests main.py
```

## Результаты

- **Тесты:** 58 passed
- **Покрытие:** 100%
- **flake8:** OK
- **mypy:** OK (strict)
- **isort:** OK
