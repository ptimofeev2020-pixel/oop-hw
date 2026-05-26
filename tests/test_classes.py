"""Тесты классов Product, Smartphone, LawnGrass и Category."""

from unittest.mock import patch

import pytest

from src.classes import Category, CategoryIterator, LawnGrass, Product, Smartphone


@pytest.fixture(autouse=True)
def reset_counters() -> None:  # type: ignore[misc]
    """Сбрасывает счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


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
    """Тесты строкового представления Product."""

    def test_str_format(self) -> None:
        p = Product("Телефон", "Описание", 80.0, 15)
        assert str(p) == "Телефон, 80.0 руб. Остаток: 15 шт."

    def test_str_with_float_price(self) -> None:
        p = Product("Товар", "Описание", 99.99, 3)
        assert str(p) == "Товар, 99.99 руб. Остаток: 3 шт."

    def test_str_zero_quantity(self) -> None:
        p = Product("Товар", "Описание", 100.0, 0)
        assert str(p) == "Товар, 100.0 руб. Остаток: 0 шт."


# ---------------------------------------------------------------------------
# Тесты Product — __add__
# ---------------------------------------------------------------------------


class TestProductAdd:
    """Тесты магического метода сложения Product."""

    def test_add_basic(self) -> None:
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 2)
        assert a + b == 1400.0

    def test_add_returns_float(self) -> None:
        a = Product("A", "О", 50.0, 5)
        b = Product("B", "О", 30.0, 3)
        assert isinstance(a + b, float)

    def test_add_symmetric(self) -> None:
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 2)
        assert a + b == b + a

    def test_add_zero_quantity(self) -> None:
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 0)
        assert a + b == 1000.0

    def test_add_same_type_smartphone(self) -> None:
        """Сложение двух смартфонов работает."""
        s1 = Smartphone("S1", "О", 100.0, 10, 90.0, "Model1", 128, "Чёрный")
        s2 = Smartphone("S2", "О", 200.0, 5, 95.0, "Model2", 256, "Белый")
        assert s1 + s2 == 2000.0

    def test_add_same_type_lawngrass(self) -> None:
        """Сложение двух газонных трав работает."""
        g1 = LawnGrass("G1", "О", 50.0, 20, "Россия", "2 недели", "Зелёный")
        g2 = LawnGrass("G2", "О", 30.0, 10, "Голландия", "3 недели", "Тёмно-зелёный")
        assert g1 + g2 == 1300.0

    def test_add_different_types_raises_error(self) -> None:
        """Сложение смартфона и газонной травы выбрасывает TypeError."""
        s = Smartphone("S1", "О", 100.0, 10, 90.0, "Model1", 128, "Чёрный")
        g = LawnGrass("G1", "О", 50.0, 20, "Россия", "2 недели", "Зелёный")
        with pytest.raises(TypeError):
            _ = s + g  # type: ignore[operator]

    def test_add_product_and_smartphone_raises_error(self) -> None:
        """Сложение Product и Smartphone выбрасывает TypeError."""
        p = Product("P", "О", 100.0, 10)
        s = Smartphone("S", "О", 200.0, 5, 90.0, "Model", 128, "Чёрный")
        with pytest.raises(TypeError):
            _ = p + s


# ---------------------------------------------------------------------------
# Тесты Product — приватность цены
# ---------------------------------------------------------------------------


class TestProductPrice:
    """Тесты приватного атрибута цены и геттера/сеттера."""

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
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_negative_prints_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = -10.0
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

    def test_price_setter_lower_any_input_declines(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        with patch("builtins.input", return_value="maybe"):
            p.price = 300.0
        assert p.price == 500.0

    def test_price_setter_no_returns(self) -> None:
        p = Product("Товар", "Описание", 500.0, 1)
        result = type(p).__dict__["price"].fset(p, 600.0)  # type: ignore[union-attr]
        assert result is None


# ---------------------------------------------------------------------------
# Тесты Product — класс-метод new_product
# ---------------------------------------------------------------------------


class TestNewProduct:
    """Тесты класс-метода new_product."""

    def test_new_product_returns_product(self) -> None:
        data = {"name": "Товар", "description": "Описание", "price": 100.0, "quantity": 5}
        p = Product.new_product(data)
        assert isinstance(p, Product)

    def test_new_product_attributes(self) -> None:
        data = {"name": "Телефон", "description": "Крутой", "price": 50000.0, "quantity": 10}
        p = Product.new_product(data)
        assert p.name == "Телефон"
        assert p.description == "Крутой"
        assert p.price == 50000.0
        assert p.quantity == 10

    def test_new_product_no_duplicates(self) -> None:
        existing = [Product("Другой", "Описание", 200.0, 3)]
        data = {"name": "Новый", "description": "Описание", "price": 100.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.name == "Новый"

    def test_new_product_duplicate_merges_quantity(self) -> None:
        existing = [Product("Телефон", "Описание", 50000.0, 10)]
        data = {"name": "Телефон", "description": "Описание", "price": 45000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.quantity == 15

    def test_new_product_duplicate_picks_max_price(self) -> None:
        existing = [Product("Телефон", "Описание", 50000.0, 10)]
        data = {"name": "Телефон", "description": "Описание", "price": 60000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.price == 60000.0

    def test_new_product_duplicate_returns_existing(self) -> None:
        existing_p = Product("Телефон", "Описание", 50000.0, 10)
        data = {"name": "Телефон", "description": "Описание", "price": 45000.0, "quantity": 5}
        p = Product.new_product(data, [existing_p])
        assert p is existing_p

    def test_new_product_is_classmethod(self) -> None:
        assert isinstance(Product.__dict__["new_product"], classmethod)


# ---------------------------------------------------------------------------
# Тесты Smartphone
# ---------------------------------------------------------------------------


class TestSmartphone:
    """Тесты класса Smartphone."""

    def test_is_subclass_of_product(self) -> None:
        """Smartphone наследуется от Product."""
        assert issubclass(Smartphone, Product)

    def test_smartphone_init(self) -> None:
        """Все атрибуты инициализируются корректно."""
        s = Smartphone("iPhone 15", "512GB", 210000.0, 8, 98.5, "iPhone 15 Pro", 512, "Gray")
        assert s.name == "iPhone 15"
        assert s.description == "512GB"
        assert s.price == 210000.0
        assert s.quantity == 8
        assert s.efficiency == 98.5
        assert s.model == "iPhone 15 Pro"
        assert s.memory == 512
        assert s.color == "Gray"

    def test_smartphone_is_product_instance(self) -> None:
        """Smartphone — экземпляр Product."""
        s = Smartphone("S", "О", 100.0, 1, 90.0, "M", 128, "Чёрный")
        assert isinstance(s, Product)

    def test_smartphone_str(self) -> None:
        """__str__ наследуется от Product."""
        s = Smartphone("iPhone", "О", 100.0, 5, 90.0, "M", 128, "Чёрный")
        assert str(s) == "iPhone, 100.0 руб. Остаток: 5 шт."


# ---------------------------------------------------------------------------
# Тесты LawnGrass
# ---------------------------------------------------------------------------


class TestLawnGrass:
    """Тесты класса LawnGrass."""

    def test_is_subclass_of_product(self) -> None:
        """LawnGrass наследуется от Product."""
        assert issubclass(LawnGrass, Product)

    def test_lawngrass_init(self) -> None:
        """Все атрибуты инициализируются корректно."""
        g = LawnGrass("Газон Элит", "Для сада", 500.0, 20, "Голландия", "2 недели", "Зелёный")
        assert g.name == "Газон Элит"
        assert g.description == "Для сада"
        assert g.price == 500.0
        assert g.quantity == 20
        assert g.country == "Голландия"
        assert g.germination_period == "2 недели"
        assert g.color == "Зелёный"

    def test_lawngrass_is_product_instance(self) -> None:
        """LawnGrass — экземпляр Product."""
        g = LawnGrass("G", "О", 50.0, 10, "Россия", "3 недели", "Зелёный")
        assert isinstance(g, Product)

    def test_lawngrass_str(self) -> None:
        """__str__ наследуется от Product."""
        g = LawnGrass("Газон", "О", 50.0, 10, "Россия", "3 недели", "Зелёный")
        assert str(g) == "Газон, 50.0 руб. Остаток: 10 шт."


# ---------------------------------------------------------------------------
# Тесты Category — инициализация
# ---------------------------------------------------------------------------


class TestCategoryInit:
    """Тесты инициализации объектов класса Category."""

    def test_category_name(self) -> None:
        cat = Category("Электроника", "Все виды электроники", [])
        assert cat.name == "Электроника"

    def test_category_description(self) -> None:
        cat = Category("Электроника", "Все виды электроники", [])
        assert cat.description == "Все виды электроники"

    def test_category_empty_products(self) -> None:
        cat = Category("Пустая", "Описание", [])
        assert cat.products == ""

    def test_products_is_private(self) -> None:
        cat = Category("Кат", "Описание", [])
        with pytest.raises(AttributeError):
            _ = cat.__products  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Тесты Category — __str__
# ---------------------------------------------------------------------------


class TestCategoryStr:
    """Тесты строкового представления Category."""

    def test_str_format(self) -> None:
        p1 = Product("Т1", "О", 100.0, 10)
        p2 = Product("Т2", "О", 200.0, 5)
        cat = Category("Электроника", "Описание", [p1, p2])
        assert str(cat) == "Электроника, количество продуктов: 15 шт."

    def test_str_empty_category(self) -> None:
        cat = Category("Пустая", "Описание", [])
        assert str(cat) == "Пустая, количество продуктов: 0 шт."

    def test_str_single_product(self) -> None:
        p = Product("Товар", "О", 100.0, 200)
        cat = Category("Кат", "Описание", [p])
        assert str(cat) == "Кат, количество продуктов: 200 шт."


# ---------------------------------------------------------------------------
# Тесты Category — products геттер
# ---------------------------------------------------------------------------


class TestCategoryProductsGetter:
    """Тесты геттера products."""

    def test_products_returns_string(self) -> None:
        p = Product("Товар", "Описание", 100.0, 5)
        cat = Category("Кат", "Описание", [p])
        assert isinstance(cat.products, str)

    def test_products_format_single(self) -> None:
        p = Product("Телефон", "Описание", 80.0, 15)
        cat = Category("Кат", "Описание", [p])
        assert cat.products == "Телефон, 80.0 руб. Остаток: 15 шт.\n"

    def test_products_format_multiple(self) -> None:
        p1 = Product("Телефон", "Описание", 80.0, 15)
        p2 = Product("Планшет", "Описание", 200.0, 3)
        cat = Category("Кат", "Описание", [p1, p2])
        expected = "Телефон, 80.0 руб. Остаток: 15 шт.\nПланшет, 200.0 руб. Остаток: 3 шт.\n"
        assert cat.products == expected

    def test_products_getter_name(self) -> None:
        assert isinstance(Category.__dict__["products"], property)


# ---------------------------------------------------------------------------
# Тесты Category — add_product
# ---------------------------------------------------------------------------


class TestCategoryAddProduct:
    """Тесты метода add_product."""

    def test_add_product_increases_list(self) -> None:
        cat = Category("Кат", "Описание", [])
        p = Product("Товар", "Описание", 100.0, 1)
        cat.add_product(p)
        assert "Товар" in cat.products

    def test_add_product_returns_none(self) -> None:
        cat = Category("Кат", "Описание", [])
        p = Product("Товар", "Описание", 100.0, 1)
        assert cat.add_product(p) is None

    def test_add_product_increments_product_count(self) -> None:
        cat = Category("Кат", "Описание", [])
        cat.add_product(Product("Товар", "Описание", 100.0, 1))
        assert Category.product_count == 1

    def test_add_product_multiple(self) -> None:
        cat = Category("Кат", "Описание", [])
        cat.add_product(Product("Т1", "О", 100.0, 1))
        cat.add_product(Product("Т2", "О", 200.0, 2))
        assert "Т1" in cat.products
        assert "Т2" in cat.products

    def test_add_smartphone(self) -> None:
        """Можно добавить Smartphone (наследник Product)."""
        cat = Category("Кат", "Описание", [])
        s = Smartphone("S", "О", 100.0, 1, 90.0, "M", 128, "Чёрный")
        cat.add_product(s)
        assert "S" in cat.products

    def test_add_lawngrass(self) -> None:
        """Можно добавить LawnGrass (наследник Product)."""
        cat = Category("Кат", "Описание", [])
        g = LawnGrass("G", "О", 50.0, 10, "Россия", "3 недели", "Зелёный")
        cat.add_product(g)
        assert "G" in cat.products

    def test_add_non_product_raises_error(self) -> None:
        """Нельзя добавить объект, не являющийся Product."""
        cat = Category("Кат", "Описание", [])
        with pytest.raises(TypeError):
            cat.add_product("не товар")  # type: ignore[arg-type]

    def test_add_dict_raises_error(self) -> None:
        """Нельзя добавить словарь вместо Product."""
        cat = Category("Кат", "Описание", [])
        with pytest.raises(TypeError):
            cat.add_product({"name": "Товар"})  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Тесты CategoryIterator
# ---------------------------------------------------------------------------


class TestCategoryIterator:
    """Тесты класса CategoryIterator."""

    def test_iterator_returns_products(self) -> None:
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        cat = Category("Кат", "Описание", [p1, p2])
        products = list(CategoryIterator(cat))
        assert len(products) == 2

    def test_iterator_empty_category(self) -> None:
        cat = Category("Кат", "Описание", [])
        assert list(CategoryIterator(cat)) == []

    def test_iterator_in_for_loop(self) -> None:
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        cat = Category("Кат", "Описание", [p1, p2])
        names = [p.name for p in CategoryIterator(cat)]
        assert names == ["Т1", "Т2"]

    def test_iterator_raises_stop_iteration(self) -> None:
        p = Product("Товар", "О", 100.0, 1)
        cat = Category("Кат", "Описание", [p])
        it = CategoryIterator(cat)
        next(it)
        with pytest.raises(StopIteration):
            next(it)

    def test_iter_returns_self(self) -> None:
        cat = Category("Кат", "Описание", [])
        it = CategoryIterator(cat)
        assert iter(it) is it


# ---------------------------------------------------------------------------
# Тесты атрибутов класса (category_count, product_count)
# ---------------------------------------------------------------------------


class TestCategoryCount:
    """Тесты подсчёта количества категорий."""

    def test_initial_count_zero(self) -> None:
        assert Category.category_count == 0

    def test_single_category(self) -> None:
        Category("Кат1", "Описание", [])
        assert Category.category_count == 1

    def test_multiple_categories(self) -> None:
        Category("Кат1", "Описание", [])
        Category("Кат2", "Описание", [])
        Category("Кат3", "Описание", [])
        assert Category.category_count == 3

    def test_count_accessible_from_instance(self) -> None:
        cat = Category("Кат1", "Описание", [])
        assert cat.category_count == 1


class TestProductCount:
    """Тесты подсчёта количества товаров."""

    def test_initial_count_zero(self) -> None:
        assert Category.product_count == 0

    def test_count_with_products(self) -> None:
        p1 = Product("Товар1", "Описание", 100.0, 1)
        p2 = Product("Товар2", "Описание", 200.0, 2)
        Category("Кат1", "Описание", [p1, p2])
        assert Category.product_count == 2

    def test_count_multiple_categories(self) -> None:
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        p3 = Product("Т3", "О", 300.0, 3)
        Category("Кат1", "Описание", [p1, p2])
        Category("Кат2", "Описание", [p3])
        assert Category.product_count == 3

    def test_empty_category_no_products(self) -> None:
        Category("Пустая", "Описание", [])
        assert Category.product_count == 0

    def test_count_accessible_from_instance(self) -> None:
        p = Product("Товар", "Описание", 100.0, 1)
        cat = Category("Кат", "Описание", [p])
        assert cat.product_count == 1
