"""Модуль с классами Product и Category для интернет-магазина."""

from abc import ABC, abstractmethod
from typing import Any


class ZeroQuantityError(Exception):
    """Исключение при попытке добавить товар с нулевым количеством."""

    def __init__(self, message: str = "Товар с нулевым количеством не может быть добавлен") -> None:
        self.message = message
        super().__init__(self.message)


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass


class PrintMixin:
    """Миксин для вывода информации о создании объекта в консоль."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self) -> str:
        attrs = ", ".join(f"{v!r}" for v in self.__dict__.values())
        return f"{self.__class__.__name__}({attrs})"


class Product(PrintMixin, BaseProduct):
    """Класс, представляющий товар в интернет-магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """Инициализирует объект товара.

        Raises:
            ValueError: Если количество равно нулю.
        """
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__(name, description, price, quantity)

    @classmethod
    def new_product(
        cls, product_data: dict[str, Any], existing_products: list["Product"] | None = None
    ) -> "Product":
        """Создаёт новый объект Product из словаря."""
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
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "BaseProduct") -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        if not isinstance(other, Product):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if value < self.__price:
            confirm = input(
                f"Вы уверены, что хотите понизить цену с {self.__price} до {value}? (y/n): "
            )
            if confirm.lower() != "y":
                return
        self.__price = value


class Smartphone(Product):
    """Класс «Смартфон» — наследник Product."""

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
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс «Трава газонная» — наследник Product."""

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
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class BaseCategory(ABC):
    """Абстрактный базовый класс для категорий и заказов."""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass


class Category(BaseCategory):
    """Класс, представляющий категорию товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию.

        Raises:
            TypeError: Если объект не является экземпляром Product.
            ZeroQuantityError: Если у товара нулевое количество.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        try:
            if product.quantity == 0:
                raise ZeroQuantityError()
        except ZeroQuantityError as e:
            print(str(e))
        else:
            self.__products.append(product)
            Category.product_count += 1
            print("Товар добавлен")
        finally:
            print("Обработка добавления товара завершена")

    def middle_price(self) -> float:
        """Подсчитывает средний ценник всех товаров в категории.

        Returns:
            Средняя цена товаров. Если товаров нет — возвращает 0.
        """
        try:
            return sum(p.price for p in self.__products) / len(self.__products)
        except ZeroDivisionError:
            return 0.0

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    @property
    def products(self) -> str:
        result = ""
        for product in self.__products:
            result += f"{product}\n"
        return result

    @property
    def products_list(self) -> list[Product]:
        return self.__products


class Order(BaseCategory):
    """Класс «Заказ» — содержит один товар, количество и итоговую стоимость."""

    def __init__(self, product: Product, buy_count: int) -> None:
        self.product = product
        self.buy_count = buy_count
        self.total_price = product.price * buy_count

    def add_product(self, product: Product) -> None:
        """Заменяет товар в заказе.

        Raises:
            TypeError: Если объект не является экземпляром Product.
            ZeroQuantityError: Если у товара нулевое количество.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product или его наследников")
        try:
            if product.quantity == 0:
                raise ZeroQuantityError()
        except ZeroQuantityError as e:
            print(str(e))
        else:
            self.product = product
            self.total_price = product.price * self.buy_count
            print("Товар добавлен")
        finally:
            print("Обработка добавления товара завершена")

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, количество: {self.buy_count}, итого: {self.total_price} руб."


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: Category) -> None:
        self._products = category.products_list
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> Product:
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product
