"""Модуль с классами Product и Category для интернет-магазина."""


class Product:
    """Класс, представляющий товар в интернет-магазине.

    Attributes:
        name: Название товара.
        description: Описание товара.
        price: Цена товара (в рублях, с копейками).
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
        self.price = price
        self.quantity = quantity


class Category:
    """Класс, представляющий категорию товаров.

    Attributes:
        name: Название категории.
        description: Описание категории.
        products: Список товаров (объектов Product) в категории.

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
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)
