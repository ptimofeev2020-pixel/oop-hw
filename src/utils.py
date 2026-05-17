"""Утилиты для загрузки данных из JSON-файла."""

import json
from typing import Any

from src.classes import Category, Product


def load_from_json(path: str) -> list[Category]:
    """Читает JSON-файл и создаёт объекты Category и Product.

    Ожидаемая структура JSON — список категорий, каждая содержит
    вложенный список товаров.

    Args:
        path: Путь до JSON-файла.

    Returns:
        Список объектов Category с вложенными объектами Product.
    """
    with open(path, encoding="utf-8") as f:
        data: list[dict[str, Any]] = json.load(f)

    categories: list[Category] = []
    for cat_data in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=p["price"],
                quantity=p["quantity"],
            )
            for p in cat_data.get("products", [])
        ]
        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products,
        )
        categories.append(category)
    return categories
