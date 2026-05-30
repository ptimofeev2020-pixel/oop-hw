"""Тесты классов Product, Smartphone, LawnGrass, Category, Order."""

from abc import ABC
from unittest.mock import patch

import pytest

from src.classes import (
    BaseCategory,
    BaseProduct,
    Category,
    CategoryIterator,
    LawnGrass,
    Order,
    PrintMixin,
    Product,
    Smartphone,
)


@pytest.fixture(autouse=True)
def reset_counters() -> None:  # type: ignore[misc]
    """Сбрасывает счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# ---------------------------------------------------------------------------
# Тесты BaseProduct
# ---------------------------------------------------------------------------


class TestBaseProduct:
    """Тесты абстрактного класса BaseProduct."""

    def test_is_abstract(self) -> None:
        """BaseProduct — абстрактный класс."""
        assert issubclass(BaseProduct, ABC)

    def test_cannot_instantiate(self) -> None:
        """Нельзя создать экземпляр BaseProduct напрямую."""
        with pytest.raises(TypeError):
            BaseProduct("T", "O", 100.0, 1)  # type: ignore[abstract]

    def test_product_inherits_base(self) -> None:
        """Product наследуется от BaseProduct."""
        assert issubclass(Product, BaseProduct)


# ---------------------------------------------------------------------------
# Тесты PrintMixin
# ---------------------------------------------------------------------------


class TestPrintMixin:
    """Тесты миксина PrintMixin."""

    def test_prints_on_creation(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Миксин печатает repr при создании объекта."""
        Product("Товар", "Описание", 100.0, 5)
        captured = capsys.readouterr()
        assert "Product(" in captured.out

    def test_repr_contains_class_name(self) -> None:
        """repr содержит имя класса."""
        p = Product("Товар", "Описание", 100.0, 5)
        assert repr(p).startswith("Product(")

    def test_repr_smartphone(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Миксин печатает имя класса Smartphone."""
        Smartphone("S", "О", 100.0, 1, 90.0, "M", 128, "Чёрный")
        captured = capsys.readouterr()
        assert "Smartphone(" in captured.out

    def test_mixin_in_product_mro(self) -> None:
        """PrintMixin в цепочке наследования Product."""
        assert PrintMixin in Product.__mro__


# ---------------------------------------------------------------------------
# Тесты Product — инициализация
# ---------------------------------------------------------------------------


class TestProductInit:
    """Тесты инициализации объектов класса Product."""

    def test_product_name(self) -> None:
        p = Product("Телефон", "Описание", 50000.0, 10)
        assert p.name == "Телефон"

    def test_product_description(self) -> None:
        p = Product("Телефон", "Супер телефон", 50000.0, 10)
        assert p.description == "Супер телефон"

    def test_product_price(self) -> None:
        p = Product("Телефон", "Описание", 49999.99, 10)
        assert p.price == 49999.99

    def test_product_quantity(self) -> None:
        p = Product("Телефон", "Описание", 50000.0, 25)
        assert p.quantity == 25

    def test_product_all_attributes(self) -> None:
        p = Product("Samsung", "Galaxy S23", 180000.0, 5)
        assert p.name == "Samsung"
        assert p.description == "Galaxy S23"
        assert p.price == 180000.0
        assert p.quantity == 5

    def test_product_zero_quantity(self) -> None:
        p = Product("Товар", "Описание", 100.0, 0)
        assert p.quantity == 0

    def test_product_price_type(self) -> None:
        p = Product("Товар", "Описание", 100.50, 1)
        assert isinstance(p.price, float)

    def test_product_quantity_type(self) -> None:
        p = Product("Товар", "Описание", 100.0, 3)
        assert isinstance(p.quantity, int)


# ---------------------------------------------------------------------------
# Тесты Product — __str__
# ---------------------------------------------------------------------------


class TestProductStr:
    def test_str_format(self) -> None:
        p = Product("Телефон", "Описание", 80.0, 15)
        assert str(p) == "Телефон, 80.0 руб. Остаток: 15 шт."

    def test_str_with_float_price(self) -> None:
        p = Product("Товар", "Описание", 99.99, 3)
        assert str(p) == "Товар, 99.99 руб. Остаток: 3 шт."


# ---------------------------------------------------------------------------
# Тесты Product — __add__
# ---------------------------------------------------------------------------


class TestProductAdd:
    def test_add_basic(self) -> None:
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 2)
        assert a + b == 1400.0

    def test_add_returns_float(self) -> None:
        a = Product("A", "О", 50.0, 5)
        b = Product("B", "О", 30.0, 3)
        assert isinstance(a + b, float)

    def test_add_same_type_smartphone(self) -> None:
        s1 = Smartphone("S1", "О", 100.0, 10, 90.0, "M1", 128, "Чёрный")
        s2 = Smartphone("S2", "О", 200.0, 5, 95.0, "M2", 256, "Белый")
        assert s1 + s2 == 2000.0

    def test_add_different_types_raises_error(self) -> None:
        s = Smartphone("S1", "О", 100.0, 10, 90.0, "M1", 128, "Чёрный")
        g = LawnGrass("G1", "О", 50.0, 20, "Россия", "2 нед", "Зелёный")
        with pytest.raises(TypeError):
            _ = s + g  # type: ignore[operator]

    def test_add_product_and_smartphone_raises_error(self) -> None:
        p = Product("P", "О", 100.0, 10)
        s = Smartphone("S", "О", 200.0, 5, 90.0, "M", 128, "Чёрный")
        with pytest.raises(TypeError):
            _ = p + s


# ---------------------------------------------------------------------------
# Тесты Product — приватность цены
# ---------------------------------------------------------------------------


class TestProductPrice:
    def test_price_is_private(self) -> None:
        p = Product("Товар", "Описание", 100.0, 1)
        with pytest.raises(AttributeError):
            _ = p.__price  # type: ignore[attr-defined]

    def test_price_getter(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        assert p.price == 500.0

    def test_price_setter_positive(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = 600.0
        assert p.price == 600.0

    def test_price_setter_zero(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = 0
        assert p.price == 500.0

    def test_price_setter_negative(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = -100.0
        assert p.price == 500.0

    def test_price_setter_zero_prints_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        capsys.readouterr()  # сбросить вывод миксина
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_lower_confirmed(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        with patch("builtins.input", return_value="y"):
            p.price = 300.0
        assert p.price == 300.0

    def test_price_setter_lower_declined(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        with patch("builtins.input", return_value="n"):
            p.price = 300.0
        assert p.price == 500.0


# ---------------------------------------------------------------------------
# Тесты Product — класс-метод new_product
# ---------------------------------------------------------------------------


class TestNewProduct:
    def test_new_product_returns_product(self) -> None:
        data = {"name": "Товар", "description": "О", "price": 100.0, "quantity": 5}
        p = Product.new_product(data)
        assert isinstance(p, Product)

    def test_new_product_attributes(self) -> None:
        data = {"name": "Телефон", "description": "Крутой", "price": 50000.0, "quantity": 10}
        p = Product.new_product(data)
        assert p.name == "Телефон"
        assert p.price == 50000.0

    def test_new_product_duplicate_merges_quantity(self) -> None:
        existing = [Product("Телефон", "О", 50000.0, 10)]
        data = {"name": "Телефон", "description": "О", "price": 45000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.quantity == 15

    def test_new_product_duplicate_picks_max_price(self) -> None:
        existing = [Product("Телефон", "О", 50000.0, 10)]
        data = {"name": "Телефон", "description": "О", "price": 60000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.price == 60000.0

    def test_new_product_is_classmethod(self) -> None:
        assert isinstance(Product.__dict__["new_product"], classmethod)


# ---------------------------------------------------------------------------
# Тесты Smartphone
# ---------------------------------------------------------------------------


class TestSmartphone:
    def test_is_subclass_of_product(self) -> None:
        assert issubclass(Smartphone, Product)

    def test_smartphone_init(self) -> None:
        s = Smartphone("iPhone 15", "512GB", 210000.0, 8, 98.5, "iPhone 15 Pro", 512, "Gray")
        assert s.name == "iPhone 15"
        assert s.efficiency == 98.5
        assert s.model == "iPhone 15 Pro"
        assert s.memory == 512
        assert s.color == "Gray"

    def test_smartphone_str(self) -> None:
        s = Smartphone("iPhone", "О", 100.0, 5, 90.0, "M", 128, "Чёрный")
        assert str(s) == "iPhone, 100.0 руб. Остаток: 5 шт."


# ---------------------------------------------------------------------------
# Тесты LawnGrass
# ---------------------------------------------------------------------------


class TestLawnGrass:
    def test_is_subclass_of_product(self) -> None:
        assert issubclass(LawnGrass, Product)

    def test_lawngrass_init(self) -> None:
        g = LawnGrass("Газон Элит", "Для сада", 500.0, 20, "Голландия", "2 нед", "Зелёный")
        assert g.country == "Голландия"
        assert g.germination_period == "2 нед"
        assert g.color == "Зелёный"

    def test_lawngrass_str(self) -> None:
        g = LawnGrass("Газон", "О", 50.0, 10, "Россия", "3 нед", "Зелёный")
        assert str(g) == "Газон, 50.0 руб. Остаток: 10 шт."


# ---------------------------------------------------------------------------
# Тесты Category
# ---------------------------------------------------------------------------


class TestCategoryInit:
    def test_category_name(self) -> None:
        cat = Category("Электроника", "Все виды электроники", [])
        assert cat.name == "Электроника"

    def test_products_is_private(self) -> None:
        cat = Category("Кат", "Описание", [])
        with pytest.raises(AttributeError):
            _ = cat.__products  # type: ignore[attr-defined]


class TestCategoryStr:
    def test_str_format(self) -> None:
        p1 = Product("Т1", "О", 100.0, 10)
        p2 = Product("Т2", "О", 200.0, 5)
        cat = Category("Электроника", "О", [p1, p2])
        assert str(cat) == "Электроника, количество продуктов: 15 шт."

    def test_str_empty_category(self) -> None:
        cat = Category("Пустая", "О", [])
        assert str(cat) == "Пустая, количество продуктов: 0 шт."


class TestCategoryProductsGetter:
    def test_products_returns_string(self) -> None:
        p = Product("Товар", "О", 100.0, 5)
        cat = Category("Кат", "О", [p])
        assert isinstance(cat.products, str)

    def test_products_format_single(self) -> None:
        p = Product("Телефон", "О", 80.0, 15)
        cat = Category("Кат", "О", [p])
        assert cat.products == "Телефон, 80.0 руб. Остаток: 15 шт.\n"


class TestCategoryAddProduct:
    def test_add_product_increases_list(self) -> None:
        cat = Category("Кат", "О", [])
        cat.add_product(Product("Товар", "О", 100.0, 1))
        assert "Товар" in cat.products

    def test_add_product_returns_none(self) -> None:
        cat = Category("Кат", "О", [])
        assert cat.add_product(Product("Товар", "О", 100.0, 1)) is None

    def test_add_product_increments_count(self) -> None:
        cat = Category("Кат", "О", [])
        cat.add_product(Product("Товар", "О", 100.0, 1))
        assert Category.product_count == 1

    def test_add_smartphone(self) -> None:
        cat = Category("Кат", "О", [])
        cat.add_product(Smartphone("S", "О", 100.0, 1, 90.0, "M", 128, "Ч"))
        assert "S" in cat.products

    def test_add_non_product_raises_error(self) -> None:
        cat = Category("Кат", "О", [])
        with pytest.raises(TypeError):
            cat.add_product("не товар")  # type: ignore[arg-type]

    def test_category_inherits_base(self) -> None:
        """Category наследуется от BaseCategory."""
        assert issubclass(Category, BaseCategory)


# ---------------------------------------------------------------------------
# Тесты Order
# ---------------------------------------------------------------------------


class TestOrder:
    def test_order_init(self) -> None:
        """Заказ инициализируется с правильными атрибутами."""
        p = Product("Товар", "О", 100.0, 10)
        order = Order(p, 3)
        assert order.product is p
        assert order.buy_count == 3
        assert order.total_price == 300.0

    def test_order_str(self) -> None:
        """Строковое представление заказа."""
        p = Product("Телефон", "О", 50000.0, 5)
        order = Order(p, 2)
        assert str(order) == "Заказ: Телефон, количество: 2, итого: 100000.0 руб."

    def test_order_add_product(self) -> None:
        """add_product заменяет товар в заказе."""
        p1 = Product("Т1", "О", 100.0, 10)
        p2 = Product("Т2", "О", 200.0, 5)
        order = Order(p1, 3)
        order.add_product(p2)
        assert order.product is p2
        assert order.total_price == 600.0

    def test_order_add_non_product_raises_error(self) -> None:
        """Нельзя добавить не-Product в заказ."""
        p = Product("Товар", "О", 100.0, 10)
        order = Order(p, 3)
        with pytest.raises(TypeError):
            order.add_product("строка")  # type: ignore[arg-type]

    def test_order_inherits_base(self) -> None:
        """Order наследуется от BaseCategory."""
        assert issubclass(Order, BaseCategory)


# ---------------------------------------------------------------------------
# Тесты CategoryIterator
# ---------------------------------------------------------------------------


class TestCategoryIterator:
    def test_iterator_returns_products(self) -> None:
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        cat = Category("Кат", "О", [p1, p2])
        assert len(list(CategoryIterator(cat))) == 2

    def test_iterator_empty_category(self) -> None:
        cat = Category("Кат", "О", [])
        assert list(CategoryIterator(cat)) == []

    def test_iterator_raises_stop_iteration(self) -> None:
        p = Product("Товар", "О", 100.0, 1)
        cat = Category("Кат", "О", [p])
        it = CategoryIterator(cat)
        next(it)
        with pytest.raises(StopIteration):
            next(it)

    def test_iter_returns_self(self) -> None:
        cat = Category("Кат", "О", [])
        it = CategoryIterator(cat)
        assert iter(it) is it


# ---------------------------------------------------------------------------
# Тесты category_count и product_count
# ---------------------------------------------------------------------------


class TestCategoryCount:
    def test_initial_count_zero(self) -> None:
        assert Category.category_count == 0

    def test_single_category(self) -> None:
        Category("Кат1", "О", [])
        assert Category.category_count == 1

    def test_multiple_categories(self) -> None:
        Category("Кат1", "О", [])
        Category("Кат2", "О", [])
        assert Category.category_count == 2


class TestProductCount:
    def test_initial_count_zero(self) -> None:
        assert Category.product_count == 0

    def test_count_with_products(self) -> None:
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        Category("Кат1", "О", [p1, p2])
        assert Category.product_count == 2

    def test_empty_category_no_products(self) -> None:
        Category("Пустая", "О", [])
        assert Category.product_count == 0
