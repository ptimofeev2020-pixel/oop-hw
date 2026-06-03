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
    ZeroQuantityError,
)


@pytest.fixture(autouse=True)
def reset_counters() -> None:  # type: ignore[misc]
    """Сбрасывает счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# ---------------------------------------------------------------------------
# Тесты ZeroQuantityError
# ---------------------------------------------------------------------------


class TestZeroQuantityError:
    def test_is_exception(self) -> None:
        assert issubclass(ZeroQuantityError, Exception)

    def test_default_message(self) -> None:
        e = ZeroQuantityError()
        assert str(e) == "Товар с нулевым количеством не может быть добавлен"

    def test_custom_message(self) -> None:
        e = ZeroQuantityError("custom")
        assert str(e) == "custom"


# ---------------------------------------------------------------------------
# Тесты BaseProduct
# ---------------------------------------------------------------------------


class TestBaseProduct:
    def test_is_abstract(self) -> None:
        assert issubclass(BaseProduct, ABC)

    def test_cannot_instantiate(self) -> None:
        with pytest.raises(TypeError):
            BaseProduct("T", "O", 100.0, 1)  # type: ignore[abstract]

    def test_product_inherits_base(self) -> None:
        assert issubclass(Product, BaseProduct)


# ---------------------------------------------------------------------------
# Тесты PrintMixin
# ---------------------------------------------------------------------------


class TestPrintMixin:
    def test_prints_on_creation(self, capsys: pytest.CaptureFixture[str]) -> None:
        Product("Товар", "Описание", 100.0, 5)
        captured = capsys.readouterr()
        assert "Product(" in captured.out

    def test_repr_contains_class_name(self) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        assert repr(p).startswith("Product(")

    def test_mixin_in_product_mro(self) -> None:
        assert PrintMixin in Product.__mro__


# ---------------------------------------------------------------------------
# Тесты Product — инициализация
# ---------------------------------------------------------------------------


class TestProductInit:
    def test_product_name(self) -> None:
        p = Product("Телефон", "Описание", 50000.0, 10)
        assert p.name == "Телефон"

    def test_product_price(self) -> None:
        p = Product("Телефон", "Описание", 49999.99, 10)
        assert p.price == 49999.99

    def test_product_quantity(self) -> None:
        p = Product("Телефон", "Описание", 50000.0, 25)
        assert p.quantity == 25

    def test_zero_quantity_raises_valueerror(self) -> None:
        """Создание товара с quantity=0 выбрасывает ValueError."""
        with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
            Product("Товар", "Описание", 100.0, 0)

    def test_nonzero_quantity_ok(self) -> None:
        p = Product("Товар", "Описание", 100.0, 1)
        assert p.quantity == 1


# ---------------------------------------------------------------------------
# Тесты Product — __str__, __add__
# ---------------------------------------------------------------------------


class TestProductStr:
    def test_str_format(self) -> None:
        p = Product("Телефон", "Описание", 80.0, 15)
        assert str(p) == "Телефон, 80.0 руб. Остаток: 15 шт."


class TestProductAdd:
    def test_add_basic(self) -> None:
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 2)
        assert a + b == 1400.0

    def test_add_different_types_raises_error(self) -> None:
        s = Smartphone("S1", "О", 100.0, 10, 90.0, "M1", 128, "Чёрный")
        g = LawnGrass("G1", "О", 50.0, 20, "Россия", "2 нед", "Зелёный")
        with pytest.raises(TypeError):
            _ = s + g  # type: ignore[operator]


# ---------------------------------------------------------------------------
# Тесты Product — цена
# ---------------------------------------------------------------------------


class TestProductPrice:
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
# Тесты new_product
# ---------------------------------------------------------------------------


class TestNewProduct:
    def test_new_product_returns_product(self) -> None:
        data = {"name": "Товар", "description": "О", "price": 100.0, "quantity": 5}
        p = Product.new_product(data)
        assert isinstance(p, Product)

    def test_new_product_duplicate_merges(self) -> None:
        existing = [Product("Телефон", "О", 50000.0, 10)]
        data = {"name": "Телефон", "description": "О", "price": 60000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.quantity == 15
        assert p.price == 60000.0


# ---------------------------------------------------------------------------
# Тесты Smartphone
# ---------------------------------------------------------------------------


class TestSmartphone:
    def test_is_subclass_of_product(self) -> None:
        assert issubclass(Smartphone, Product)

    def test_smartphone_init(self) -> None:
        s = Smartphone("iPhone", "512GB", 210000.0, 8, 98.5, "iPhone 15", 512, "Gray")
        assert s.efficiency == 98.5
        assert s.model == "iPhone 15"
        assert s.memory == 512
        assert s.color == "Gray"

    def test_smartphone_zero_quantity_raises(self) -> None:
        with pytest.raises(ValueError):
            Smartphone("S", "О", 100.0, 0, 90.0, "M", 128, "Ч")


# ---------------------------------------------------------------------------
# Тесты LawnGrass
# ---------------------------------------------------------------------------


class TestLawnGrass:
    def test_is_subclass_of_product(self) -> None:
        assert issubclass(LawnGrass, Product)

    def test_lawngrass_init(self) -> None:
        g = LawnGrass("Газон", "Для сада", 500.0, 20, "Голландия", "2 нед", "Зелёный")
        assert g.country == "Голландия"
        assert g.germination_period == "2 нед"

    def test_lawngrass_zero_quantity_raises(self) -> None:
        with pytest.raises(ValueError):
            LawnGrass("G", "О", 50.0, 0, "Россия", "3 нед", "Зелёный")


# ---------------------------------------------------------------------------
# Тесты Category
# ---------------------------------------------------------------------------


class TestCategoryInit:
    def test_category_name(self) -> None:
        cat = Category("Электроника", "Все виды", [])
        assert cat.name == "Электроника"

    def test_products_is_private(self) -> None:
        cat = Category("Кат", "О", [])
        with pytest.raises(AttributeError):
            _ = cat.__products  # type: ignore[attr-defined]


class TestCategoryStr:
    def test_str_format(self) -> None:
        p1 = Product("Т1", "О", 100.0, 10)
        p2 = Product("Т2", "О", 200.0, 5)
        cat = Category("Электроника", "О", [p1, p2])
        assert str(cat) == "Электроника, количество продуктов: 15 шт."


class TestCategoryMiddlePrice:
    """Тесты метода middle_price."""

    def test_middle_price_basic(self) -> None:
        p1 = Product("Т1", "О", 100.0, 10)
        p2 = Product("Т2", "О", 200.0, 5)
        cat = Category("Кат", "О", [p1, p2])
        assert cat.middle_price() == 150.0

    def test_middle_price_single(self) -> None:
        p = Product("Т", "О", 300.0, 1)
        cat = Category("Кат", "О", [p])
        assert cat.middle_price() == 300.0

    def test_middle_price_empty_returns_zero(self) -> None:
        """Пустая категория — средний ценник 0."""
        cat = Category("Кат", "О", [])
        assert cat.middle_price() == 0.0


class TestCategoryAddProduct:
    def test_add_product_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        cat = Category("Кат", "О", [])
        capsys.readouterr()
        cat.add_product(Product("Товар", "О", 100.0, 5))
        captured = capsys.readouterr()
        assert "Товар добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_add_product_increments_count(self) -> None:
        cat = Category("Кат", "О", [])
        cat.add_product(Product("Товар", "О", 100.0, 1))
        assert Category.product_count == 1

    def test_add_non_product_raises_error(self) -> None:
        cat = Category("Кат", "О", [])
        with pytest.raises(TypeError):
            cat.add_product("не товар")  # type: ignore[arg-type]

    def test_add_zero_quantity_product_prints_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Добавление товара с quantity=0 (через подмену) печатает ошибку."""
        cat = Category("Кат", "О", [])
        p = Product("Товар", "О", 100.0, 5)
        p.quantity = 0  # симулируем нулевое количество
        capsys.readouterr()
        cat.add_product(p)
        captured = capsys.readouterr()
        assert "Товар с нулевым количеством не может быть добавлен" in captured.out
        assert "Обработка добавления товара завершена" in captured.out

    def test_category_inherits_base(self) -> None:
        assert issubclass(Category, BaseCategory)


# ---------------------------------------------------------------------------
# Тесты Order
# ---------------------------------------------------------------------------


class TestOrder:
    def test_order_init(self) -> None:
        p = Product("Товар", "О", 100.0, 10)
        order = Order(p, 3)
        assert order.total_price == 300.0

    def test_order_str(self) -> None:
        p = Product("Телефон", "О", 50000.0, 5)
        order = Order(p, 2)
        assert str(order) == "Заказ: Телефон, количество: 2, итого: 100000.0 руб."

    def test_order_add_product_zero_quantity(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Добавление товара с quantity=0 в заказ печатает ошибку."""
        p1 = Product("Т1", "О", 100.0, 10)
        order = Order(p1, 3)
        p2 = Product("Т2", "О", 200.0, 5)
        p2.quantity = 0
        capsys.readouterr()
        order.add_product(p2)
        captured = capsys.readouterr()
        assert "Товар с нулевым количеством не может быть добавлен" in captured.out

    def test_order_inherits_base(self) -> None:
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

    def test_iterator_raises_stop_iteration(self) -> None:
        p = Product("Товар", "О", 100.0, 1)
        cat = Category("Кат", "О", [p])
        it = CategoryIterator(cat)
        next(it)
        with pytest.raises(StopIteration):
            next(it)


# ---------------------------------------------------------------------------
# Тесты category_count, product_count
# ---------------------------------------------------------------------------


class TestCategoryCount:
    def test_initial_count_zero(self) -> None:
        assert Category.category_count == 0

    def test_single_category(self) -> None:
        Category("Кат1", "О", [])
        assert Category.category_count == 1


class TestProductCount:
    def test_count_with_products(self) -> None:
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        Category("Кат1", "О", [p1, p2])
        assert Category.product_count == 2
