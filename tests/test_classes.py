"""Тесты классов Product и Category."""

import pytest

from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_counters() -> None:  # type: ignore[misc]
    """Сбрасывает счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# ---------------------------------------------------------------------------
# Тесты Product
# ---------------------------------------------------------------------------


class TestProductInit:
    """Тесты инициализации объектов класса Product."""

    def test_product_name(self) -> None:
        """Атрибут name сохраняется корректно."""
        p = Product("Телефон", "Описание", 50000.0, 10)
        assert p.name == "Телефон"

    def test_product_description(self) -> None:
        """Атрибут description сохраняется корректно."""
        p = Product("Телефон", "Супер телефон", 50000.0, 10)
        assert p.description == "Супер телефон"

    def test_product_price(self) -> None:
        """Атрибут price сохраняется корректно (с копейками)."""
        p = Product("Телефон", "Описание", 49999.99, 10)
        assert p.price == 49999.99

    def test_product_quantity(self) -> None:
        """Атрибут quantity сохраняется корректно."""
        p = Product("Телефон", "Описание", 50000.0, 25)
        assert p.quantity == 25

    def test_product_all_attributes(self) -> None:
        """Все атрибуты товара инициализируются одновременно."""
        p = Product("Samsung", "Galaxy S23", 180000.0, 5)
        assert p.name == "Samsung"
        assert p.description == "Galaxy S23"
        assert p.price == 180000.0
        assert p.quantity == 5

    def test_product_zero_quantity(self) -> None:
        """Товар с нулевым количеством."""
        p = Product("Товар", "Описание", 100.0, 0)
        assert p.quantity == 0

    def test_product_price_type(self) -> None:
        """Цена хранится как float."""
        p = Product("Товар", "Описание", 100.50, 1)
        assert isinstance(p.price, float)

    def test_product_quantity_type(self) -> None:
        """Количество хранится как int."""
        p = Product("Товар", "Описание", 100.0, 3)
        assert isinstance(p.quantity, int)


# ---------------------------------------------------------------------------
# Тесты Category
# ---------------------------------------------------------------------------


class TestCategoryInit:
    """Тесты инициализации объектов класса Category."""

    def test_category_name(self) -> None:
        """Атрибут name сохраняется корректно."""
        cat = Category("Электроника", "Все виды электроники", [])
        assert cat.name == "Электроника"

    def test_category_description(self) -> None:
        """Атрибут description сохраняется корректно."""
        cat = Category("Электроника", "Все виды электроники", [])
        assert cat.description == "Все виды электроники"

    def test_category_products_list(self) -> None:
        """Атрибут products — список объектов Product."""
        p1 = Product("Телефон", "Описание", 50000.0, 10)
        p2 = Product("Планшет", "Описание", 30000.0, 5)
        cat = Category("Гаджеты", "Описание", [p1, p2])
        assert len(cat.products) == 2
        assert cat.products[0].name == "Телефон"
        assert cat.products[1].name == "Планшет"

    def test_category_empty_products(self) -> None:
        """Категория без товаров."""
        cat = Category("Пустая", "Описание", [])
        assert cat.products == []

    def test_products_are_product_instances(self) -> None:
        """Элементы списка products — экземпляры Product."""
        p = Product("Товар", "Описание", 100.0, 1)
        cat = Category("Категория", "Описание", [p])
        assert isinstance(cat.products[0], Product)


# ---------------------------------------------------------------------------
# Тесты атрибутов класса (category_count, product_count)
# ---------------------------------------------------------------------------


class TestCategoryCount:
    """Тесты подсчёта количества категорий."""

    def test_initial_count_zero(self) -> None:
        """До создания объектов счётчик равен 0."""
        assert Category.category_count == 0

    def test_single_category(self) -> None:
        """Создание одной категории увеличивает счётчик на 1."""
        Category("Кат1", "Описание", [])
        assert Category.category_count == 1

    def test_multiple_categories(self) -> None:
        """Создание нескольких категорий корректно считает."""
        Category("Кат1", "Описание", [])
        Category("Кат2", "Описание", [])
        Category("Кат3", "Описание", [])
        assert Category.category_count == 3

    def test_count_accessible_from_instance(self) -> None:
        """Атрибут класса доступен через экземпляр."""
        cat = Category("Кат1", "Описание", [])
        assert cat.category_count == 1


class TestProductCount:
    """Тесты подсчёта количества товаров."""

    def test_initial_count_zero(self) -> None:
        """До создания объектов счётчик товаров равен 0."""
        assert Category.product_count == 0

    def test_count_with_products(self) -> None:
        """Счётчик товаров увеличивается на количество товаров в категории."""
        p1 = Product("Товар1", "Описание", 100.0, 1)
        p2 = Product("Товар2", "Описание", 200.0, 2)
        Category("Кат1", "Описание", [p1, p2])
        assert Category.product_count == 2

    def test_count_multiple_categories(self) -> None:
        """Счётчик суммирует товары из всех категорий."""
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        p3 = Product("Т3", "О", 300.0, 3)
        Category("Кат1", "Описание", [p1, p2])
        Category("Кат2", "Описание", [p3])
        assert Category.product_count == 3

    def test_empty_category_no_products(self) -> None:
        """Пустая категория не увеличивает счётчик товаров."""
        Category("Пустая", "Описание", [])
        assert Category.product_count == 0

    def test_count_accessible_from_instance(self) -> None:
        """Атрибут product_count доступен через экземпляр."""
        p = Product("Товар", "Описание", 100.0, 1)
        cat = Category("Кат", "Описание", [p])
        assert cat.product_count == 1
