"""Модуль с классами Product и Category для интернет-магазина."""

from typing import Any


class Product:
    """Класс, представляющий товар в интернет-магазине.

    Attributes:
        name: Название товара.
        description: Описание товара.
        __price: Цена товара (приватный атрибут).
        quantity: Количество товара в наличии (в штуках).
    """

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует объект товара.

        Args:
            name: Название товара.
            description: Описание товара.
            price: Цена товара.
            quantity: Количество в наличии.
        """
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @classmethod
    def new_product(
        cls, product_data: dict[str, Any], existing_products: list["Product"] | None = None
    ) -> "Product":
        """Создаёт новый объект Product из словаря.

        Если в existing_products есть товар с таким же именем,
        суммирует количество и выбирает максимальную цену.

        Args:
            product_data: Словарь с ключами name, description, price, quantity.
            existing_products: Список существующих товаров для проверки дубликатов.

        Returns:
            Объект Product.
        """
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if existing_products is not None:
            for existing in existing_products:
                if existing.name == name:
                    existing.quantity += quantity
                    existing.price = max(existing.price, price)
                    return existing

        return cls(name, description, price, quantity)

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Устанавливает цену товара с валидацией.

        Если значение <= 0, выводит сообщение и не меняет цену.
        Если цена понижается, запрашивает подтверждение у пользователя.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if value < self.__price:
            confirm = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {value}? (y/n): ")
            if confirm.lower() != "y":
                return
        self.__price = value


class Category:
    """Класс, представляющий категорию товаров.

    Attributes:
        name: Название категории.
        description: Описание категории.
        __products: Список товаров (приватный атрибут).

    Class Attributes:
        category_count: Общее количество созданных категорий.
        product_count: Общее количество товаров во всех категориях.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        """Инициализирует объект категории.

        При создании автоматически увеличивает счётчик категорий
        и добавляет количество товаров к общему счётчику.

        Args:
            name: Название категории.
            description: Описание категории.
            products: Список объектов Product.
        """
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию.

        Args:
            product: Объект Product для добавления.
        """
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строку со всеми товарами в категории.

        Формат каждого товара: "Название продукта, X руб. Остаток: X шт.\\n"
        """
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    @property
    def products_list(self) -> list[Product]:
        """Возвращает список объектов Product (для внутреннего использования)."""
        return self.__products
