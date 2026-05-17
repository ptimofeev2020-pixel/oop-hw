# Домашнее задание: ООП — Интернет-магазин

Проект реализует базовые классы для интернет-магазина: `Product` и `Category`.

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

- **Тесты:** 33 passed
- **Покрытие:** 100%
- **flake8:** OK
- **mypy:** OK (strict)
- **isort:** OK
