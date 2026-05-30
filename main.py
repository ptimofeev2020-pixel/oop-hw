"""Главный модуль проекта — демонстрация работы классов."""

from src.classes import Category, LawnGrass, Order, Smartphone
from src.utils import load_from_json


def main() -> None:
    """Демонстрирует создание и использование объектов."""
    # Смартфоны (PrintMixin выведет repr при создании)
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )
    smartphone2 = Smartphone(
        "Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "iPhone 15 Pro", 512, "Gray"
    )

    # Газонная трава
    grass1 = LawnGrass("Газон Элит", "Для сада", 500.0, 20, "Голландия", "2 недели", "Зелёный")
    print(f"\n{grass1}")

    # Категория
    category = Category("Смартфоны", "Умные телефоны", [smartphone1, smartphone2])
    print(f"\n{category}")
    print(category.products)

    # Заказ
    order = Order(smartphone1, 2)
    print(order)

    # Загрузка из JSON
    print("\n--- Загрузка из JSON ---")
    categories = load_from_json("data/products.json")
    for cat in categories:
        print(f"\n{cat}")
        print(cat.products)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()
