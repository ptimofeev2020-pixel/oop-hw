"""Главный модуль проекта — демонстрация работы классов Product и Category."""

from src.classes import Category, Product
from src.utils import load_from_json


def main() -> None:
    """Демонстрирует создание и использование объектов Product и Category."""
    # Создание товаров
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создание категории
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации",
        [product1, product2, product3],
    )

    print(f"Категория: {category1.name}")
    print(f"Описание: {category1.description}")
    print(f"Товаров в категории: {len(category1.products)}")
    print()

    for product in category1.products:
        print(f"  {product.name} — {product.price} руб. (в наличии: {product.quantity} шт.)")

    print()
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Загрузка из JSON
    print("\n--- Загрузка из JSON ---")
    categories = load_from_json("data/products.json")
    for cat in categories:
        print(f"\nКатегория: {cat.name}")
        for p in cat.products:
            print(f"  {p.name} — {p.price} руб.")

    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()
