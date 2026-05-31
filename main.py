"""Главный модуль проекта — демонстрация работы классов."""

from src.classes import Category, CategoryIterator, LawnGrass, Order, Product, Smartphone
from src.utils import load_from_json


def main() -> None:
    """Демонстрирует создание и использование объектов."""
    # Создание продуктов
    product1 = Product("Продукт1", "Описание продукта", 1200.0, 10)
    product2 = Product("Продукт2", "Описание продукта2", 800.0, 5)

    # Смартфоны
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
        180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )
    smartphone2 = Smartphone(
        "Iphone 15", "512GB, Gray space",
        210000.0, 8, 98.2, "iPhone 15 Pro", 512, "Gray"
    )
    smartphone3 = Smartphone(
        "Xiaomi Redmi Note 11", "1024GB, Синий",
        31000.0, 14, 90.3, "Redmi Note 11", 1024, "Синий"
    )

    # Газонная трава
    grass1 = LawnGrass(
        "Газонная трава", "Элитная трава для газона",
        500.0, 20, "Россия", "7 дней", "Зелёный"
    )
    grass2 = LawnGrass(
        "Газонная трава 2", "Выносливая трава",
        450.0, 15, "США", "5 дней", "Тёмно-зелёный"
    )

    # Строковое представление
    print(product1)
    print(product2)
    print(smartphone1)
    print(grass1)

    # Сложение одинаковых типов
    print(f"\nСложение смартфонов: {smartphone1 + smartphone2}")
    print(f"Сложение травы: {grass1 + grass2}")

    # Сложение разных типов — ошибка
    try:
        print(smartphone1 + grass1)
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Категория
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации",
        [smartphone1, smartphone2, smartphone3],
    )
    print(f"\n{category1}")
    print(category1.products)

    # Добавление продукта
    category1.add_product(product1)

    # Попытка добавить не-Product
    try:
        category1.add_product("не товар")  # type: ignore[arg-type]
    except TypeError as e:
        print(f"Ошибка: {e}")

    # Заказ
    order = Order(smartphone1, 2)
    print(order)

    # Итератор
    print("\nПеребор через CategoryIterator:")
    for p in CategoryIterator(category1):
        print(f"  {p}")

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
