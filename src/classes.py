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

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение двух товаров — сумма стоимостей на складе.

        Складывать можно только товары одного класса (type).

        Raises:
            TypeError: Если типы товаров различаются.
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity

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


class Smartphone(Product):
    """Класс «Смартфон» — наследник Product.

    Attributes:
        efficiency: Производительность.
        model: Модель.
        memory: Объём встроенной памяти.
        color: Цвет.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        """Инициализирует смартфон."""
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс «Трава газонная» — наследник Product.

    Attributes:
        country: Страна-производитель.
        germination_period: Срок прорастания.
        color: Цвет.
    """

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        """Инициализирует траву газонную."""
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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

        Принимает только объекты Product или его наследников.

        Args:
            product: Объект Product для добавления.

        Raises:
            TypeError: Если объект не является экземпляром Product.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    def __str__(self) -> str:
        """Строковое представление категории.

        Количество продуктов — сумма quantity всех товаров на складе.
        """
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self) -> str:
        """Возвращает строку со всеми товарами в категории."""
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    @property
    def products_list(self) -> list[Product]:
        """Возвращает список объектов Product (для внутреннего использования)."""
        return self.__products


class CategoryIterator:
    """Итератор для перебора товаров в категории.

    Позволяет использовать объект Category в цикле for.
    """

    def __init__(self, category: Category) -> None:
        """Инициализирует итератор.

        Args:
            category: Объект Category для итерации.
        """
        self._products = category.products_list
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        """Возвращает сам итератор."""
        return self

    def __next__(self) -> Product:
        """Возвращает следующий товар.

        Raises:
            StopIteration: Когда товары закончились.
        """
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product
