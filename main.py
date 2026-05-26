"""Главный модуль проекта — демонстрация работы классов."""

from src.classes import Category, CategoryIterator, LawnGrass, Product, Smartphone
from src.utils import load_from_json


def main() -> None:
    """Демонстрирует создание и использование объектов."""
    # Смартфоны
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "iPhone 15 Pro", 512, "Gray")

    # Газонная трава
    grass1 = LawnGrass("Газон Элит", "Для сада", 500.0, 20, "Голландия", "2 недели", "Зелёный")
    grass2 = LawnGrass("Газон Стандарт", "Универсальный", 300.0, 50, "Россия", "3 недели", "Тёмно-зелёный")

    # Строковое представление
    print(smartphone1)
    print(grass1)

    # Сложение одинаковых типов
    total_smartphones = smartphone1 + smartphone2
    print(f"\nОбщая стоимость смартфонов на складе: {total_smartphones} руб.")

    total_grass = grass1 + grass2
    print(f"Общая стоимость газонной травы на складе: {total_grass} руб.")

    # Сложение разных типов — ошибка
    try:
        _ = smartphone1 + grass1
    except TypeError as e:
        print(f"\nОшибка при сложении разных типов: {e}")

    # Категория с проверкой типа
    category = Category("Смартфоны", "Умные телефоны", [smartphone1, smartphone2])
    print(f"\n{category}")
    print(category.products)

    # Добавление продукта
    product = Product("Чехол", "Силиконовый", 1500.0, 100)
    category.add_product(product)

    # Попытка добавить не-Product
    try:
        category.add_product("не товар")  # type: ignore[arg-type]
    except TypeError as e:
        print(f"Ошибка при добавлении: {e}")

    # Итератор
    print("\nПеребор через CategoryIterator:")
    for p in CategoryIterator(category):
        print(f"  {p}")

    print(f"\nВсего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    # Загрузка из JSON
    print("\n--- Загрузка из JSON ---")
    categories = load_from_json("data/products.json")
    for cat in categories:
        print(f"\n{cat}")
        print(cat.products)


if __name__ == "__main__":
    main()
