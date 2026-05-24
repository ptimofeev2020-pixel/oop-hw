"""Главный модуль проекта — демонстрация работы классов Product и Category."""

from src.classes import Category, CategoryIterator, Product
from src.utils import load_from_json


def main() -> None:
    """Демонстрирует создание и использование объектов Product и Category."""
    # Создание товаров
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Строковое представление товара
    print(product1)
    print(product2)

    # Сложение товаров (сумма стоимостей на складе)
    total = product1 + product2
    print(f"\nОбщая стоимость на складе: {total} руб.")

    # Создание категории
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации",
        [product1, product2, product3],
    )

    # Строковое представление категории
    print(f"\n{category1}")
    print(f"\nТовары в категории:\n{category1.products}")

    # Итератор
    print("Перебор через CategoryIterator:")
    for product in CategoryIterator(category1):
        print(f"  {product}")

    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

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
