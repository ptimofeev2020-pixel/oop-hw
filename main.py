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
    print(f"Товары в категории:\n{category1.products}")

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Добавление товара через add_product
    product4 = Product("Huawei P60", "256GB, Чёрный", 90000.0, 3)
    category1.add_product(product4)
    print(f"\nПосле добавления товара:\n{category1.products}")

    # Создание товара через класс-метод new_product
    product_data = {"name": "OnePlus 12", "description": "256GB", "price": 75000.0, "quantity": 10}
    new_p = Product.new_product(product_data)
    print(f"Новый товар: {new_p.name} — {new_p.price} руб.")

    # Проверка дубликата
    duplicate_data = {"name": "Samsung Galaxy S23 Ultra", "description": "256GB", "price": 200000.0, "quantity": 3}
    merged = Product.new_product(duplicate_data, category1.products_list)
    print(f"Объединённый товар: {merged.name} — {merged.price} руб., {merged.quantity} шт.")

    # Загрузка из JSON
    print("\n--- Загрузка из JSON ---")
    categories = load_from_json("data/products.json")
    for cat in categories:
        print(f"\nКатегория: {cat.name}")
        print(cat.products)

    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")


if __name__ == "__main__":
    main()
