"""Тесты классов Product и Category."""

from unittest.mock import patch

import pytest

from src.classes import Category, CategoryIterator, Product


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
# Тесты Product — __str__
# ---------------------------------------------------------------------------


class TestProductStr:
    """Тесты строкового представления Product."""

    def test_str_format(self) -> None:
        """__str__ возвращает строку в правильном формате."""
        p = Product("Телефон", "Описание", 80.0, 15)
        assert str(p) == "Телефон, 80.0 руб. Остаток: 15 шт."

    def test_str_with_float_price(self) -> None:
        """__str__ корректно отображает дробную цену."""
        p = Product("Товар", "Описание", 99.99, 3)
        assert str(p) == "Товар, 99.99 руб. Остаток: 3 шт."

    def test_str_zero_quantity(self) -> None:
        """__str__ для товара с нулевым количеством."""
        p = Product("Товар", "Описание", 100.0, 0)
        assert str(p) == "Товар, 100.0 руб. Остаток: 0 шт."


# ---------------------------------------------------------------------------
# Тесты Product — __add__
# ---------------------------------------------------------------------------


class TestProductAdd:
    """Тесты магического метода сложения Product."""

    def test_add_basic(self) -> None:
        """Сложение двух товаров: сумма (цена * количество)."""
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 2)
        assert a + b == 1400.0

    def test_add_returns_float(self) -> None:
        """Результат сложения — float."""
        a = Product("A", "О", 50.0, 5)
        b = Product("B", "О", 30.0, 3)
        result = a + b
        assert isinstance(result, float)

    def test_add_symmetric(self) -> None:
        """Сложение коммутативно."""
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 2)
        assert a + b == b + a

    def test_add_zero_quantity(self) -> None:
        """Сложение с товаром с нулевым количеством."""
        a = Product("A", "О", 100.0, 10)
        b = Product("B", "О", 200.0, 0)
        assert a + b == 1000.0


# ---------------------------------------------------------------------------
# Тесты Product — приватность цены
# ---------------------------------------------------------------------------


class TestProductPrice:
    """Тесты приватного атрибута цены и геттера/сеттера."""

    def test_price_is_private(self) -> None:
        """Атрибут __price недоступен напрямую."""
        p = Product("Товар", "Описание", 100.0, 1)
        with pytest.raises(AttributeError):
            _ = p.__price  # type: ignore[attr-defined]

    def test_price_getter(self) -> None:
        """Геттер price возвращает значение приватного атрибута."""
        p = Product("Товар", "Описание", 500.0, 1)
        assert p.price == 500.0

    def test_price_setter_positive(self) -> None:
        """Сеттер устанавливает новую цену, если она выше текущей."""
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = 600.0
        assert p.price == 600.0

    def test_price_setter_zero(self) -> None:
        """Сеттер не меняет цену при нулевом значении."""
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = 0
        assert p.price == 500.0

    def test_price_setter_negative(self) -> None:
        """Сеттер не меняет цену при отрицательном значении."""
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = -100.0
        assert p.price == 500.0

    def test_price_setter_zero_prints_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Сеттер выводит сообщение при нулевой цене."""
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_negative_prints_message(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Сеттер выводит сообщение при отрицательной цене."""
        p = Product("Товар", "Описание", 500.0, 1)
        p.price = -10.0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out

    def test_price_setter_lower_confirmed(self) -> None:
        """Цена понижается при подтверждении пользователем (y)."""
        p = Product("Товар", "Описание", 500.0, 1)
        with patch("builtins.input", return_value="y"):
            p.price = 300.0
        assert p.price == 300.0

    def test_price_setter_lower_declined(self) -> None:
        """Цена не понижается при отказе пользователя (n)."""
        p = Product("Товар", "Описание", 500.0, 1)
        with patch("builtins.input", return_value="n"):
            p.price = 300.0
        assert p.price == 500.0

    def test_price_setter_lower_any_input_declines(self) -> None:
        """Любой ответ, кроме 'y', отменяет понижение."""
        p = Product("Товар", "Описание", 500.0, 1)
        with patch("builtins.input", return_value="maybe"):
            p.price = 300.0
        assert p.price == 500.0

    def test_price_setter_no_returns(self) -> None:
        """Сеттер не возвращает значений."""
        p = Product("Товар", "Описание", 500.0, 1)
        result = type(p).__dict__["price"].fset(p, 600.0)  # type: ignore[union-attr]
        assert result is None


# ---------------------------------------------------------------------------
# Тесты Product — класс-метод new_product
# ---------------------------------------------------------------------------


class TestNewProduct:
    """Тесты класс-метода new_product."""

    def test_new_product_returns_product(self) -> None:
        """new_product возвращает экземпляр Product."""
        data = {"name": "Товар", "description": "Описание", "price": 100.0, "quantity": 5}
        p = Product.new_product(data)
        assert isinstance(p, Product)

    def test_new_product_attributes(self) -> None:
        """Атрибуты нового товара соответствуют словарю."""
        data = {"name": "Телефон", "description": "Крутой", "price": 50000.0, "quantity": 10}
        p = Product.new_product(data)
        assert p.name == "Телефон"
        assert p.description == "Крутой"
        assert p.price == 50000.0
        assert p.quantity == 10

    def test_new_product_no_duplicates(self) -> None:
        """Без дубликатов создаётся новый объект."""
        existing = [Product("Другой", "Описание", 200.0, 3)]
        data = {"name": "Новый", "description": "Описание", "price": 100.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.name == "Новый"
        assert len(existing) == 1

    def test_new_product_duplicate_merges_quantity(self) -> None:
        """При дубликате количество суммируется."""
        existing = [Product("Телефон", "Описание", 50000.0, 10)]
        data = {"name": "Телефон", "description": "Описание", "price": 45000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.quantity == 15

    def test_new_product_duplicate_picks_max_price(self) -> None:
        """При дубликате выбирается максимальная цена."""
        existing = [Product("Телефон", "Описание", 50000.0, 10)]
        data = {"name": "Телефон", "description": "Описание", "price": 60000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p.price == 60000.0

    def test_new_product_duplicate_returns_existing(self) -> None:
        """При дубликате возвращается существующий объект."""
        existing_p = Product("Телефон", "Описание", 50000.0, 10)
        existing = [existing_p]
        data = {"name": "Телефон", "description": "Описание", "price": 45000.0, "quantity": 5}
        p = Product.new_product(data, existing)
        assert p is existing_p

    def test_new_product_is_classmethod(self) -> None:
        """new_product является класс-методом."""
        assert isinstance(Product.__dict__["new_product"], classmethod)


# ---------------------------------------------------------------------------
# Тесты Category — инициализация
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

    def test_category_empty_products(self) -> None:
        """Категория без товаров — пустая строка."""
        cat = Category("Пустая", "Описание", [])
        assert cat.products == ""

    def test_products_is_private(self) -> None:
        """Атрибут __products недоступен напрямую."""
        cat = Category("Кат", "Описание", [])
        with pytest.raises(AttributeError):
            _ = cat.__products  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# Тесты Category — __str__
# ---------------------------------------------------------------------------


class TestCategoryStr:
    """Тесты строкового представления Category."""

    def test_str_format(self) -> None:
        """__str__ возвращает правильный формат."""
        p1 = Product("Т1", "О", 100.0, 10)
        p2 = Product("Т2", "О", 200.0, 5)
        cat = Category("Электроника", "Описание", [p1, p2])
        assert str(cat) == "Электроника, количество продуктов: 15 шт."

    def test_str_empty_category(self) -> None:
        """__str__ для пустой категории."""
        cat = Category("Пустая", "Описание", [])
        assert str(cat) == "Пустая, количество продуктов: 0 шт."

    def test_str_single_product(self) -> None:
        """__str__ для категории с одним товаром."""
        p = Product("Товар", "О", 100.0, 200)
        cat = Category("Кат", "Описание", [p])
        assert str(cat) == "Кат, количество продуктов: 200 шт."

    def test_str_calculates_total_quantity(self) -> None:
        """__str__ суммирует quantity всех товаров."""
        p1 = Product("Т1", "О", 100.0, 50)
        p2 = Product("Т2", "О", 200.0, 100)
        p3 = Product("Т3", "О", 300.0, 50)
        cat = Category("Кат", "Описание", [p1, p2, p3])
        assert str(cat) == "Кат, количество продуктов: 200 шт."


# ---------------------------------------------------------------------------
# Тесты Category — products геттер
# ---------------------------------------------------------------------------


class TestCategoryProductsGetter:
    """Тесты геттера products."""

    def test_products_returns_string(self) -> None:
        """Геттер products возвращает строку."""
        p = Product("Товар", "Описание", 100.0, 5)
        cat = Category("Кат", "Описание", [p])
        assert isinstance(cat.products, str)

    def test_products_format_single(self) -> None:
        """Формат строки для одного товара (через __str__)."""
        p = Product("Телефон", "Описание", 80.0, 15)
        cat = Category("Кат", "Описание", [p])
        assert cat.products == "Телефон, 80.0 руб. Остаток: 15 шт.\n"

    def test_products_format_multiple(self) -> None:
        """Формат строки для нескольких товаров."""
        p1 = Product("Телефон", "Описание", 80.0, 15)
        p2 = Product("Планшет", "Описание", 200.0, 3)
        cat = Category("Кат", "Описание", [p1, p2])
        expected = "Телефон, 80.0 руб. Остаток: 15 шт.\nПланшет, 200.0 руб. Остаток: 3 шт.\n"
        assert cat.products == expected

    def test_products_getter_name(self) -> None:
        """Имя метода-геттера — products."""
        assert "products" in Category.__dict__
        assert isinstance(Category.__dict__["products"], property)


# ---------------------------------------------------------------------------
# Тесты Category — add_product
# ---------------------------------------------------------------------------


class TestCategoryAddProduct:
    """Тесты метода add_product."""

    def test_add_product_increases_list(self) -> None:
        """Добавление товара увеличивает список."""
        cat = Category("Кат", "Описание", [])
        p = Product("Товар", "Описание", 100.0, 1)
        cat.add_product(p)
        assert "Товар" in cat.products

    def test_add_product_returns_none(self) -> None:
        """add_product не возвращает значений."""
        cat = Category("Кат", "Описание", [])
        p = Product("Товар", "Описание", 100.0, 1)
        result = cat.add_product(p)
        assert result is None

    def test_add_product_increments_product_count(self) -> None:
        """add_product увеличивает product_count на 1."""
        cat = Category("Кат", "Описание", [])
        assert Category.product_count == 0
        p = Product("Товар", "Описание", 100.0, 1)
        cat.add_product(p)
        assert Category.product_count == 1

    def test_add_product_multiple(self) -> None:
        """Несколько вызовов add_product добавляют все товары."""
        cat = Category("Кат", "Описание", [])
        cat.add_product(Product("Т1", "О", 100.0, 1))
        cat.add_product(Product("Т2", "О", 200.0, 2))
        assert "Т1" in cat.products
        assert "Т2" in cat.products
        assert Category.product_count == 2


# ---------------------------------------------------------------------------
# Тесты CategoryIterator
# ---------------------------------------------------------------------------


class TestCategoryIterator:
    """Тесты класса CategoryIterator."""

    def test_iterator_returns_products(self) -> None:
        """Итератор возвращает все товары."""
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        cat = Category("Кат", "Описание", [p1, p2])
        products = list(CategoryIterator(cat))
        assert len(products) == 2
        assert products[0].name == "Т1"
        assert products[1].name == "Т2"

    def test_iterator_empty_category(self) -> None:
        """Итератор для пустой категории."""
        cat = Category("Кат", "Описание", [])
        products = list(CategoryIterator(cat))
        assert products == []

    def test_iterator_in_for_loop(self) -> None:
        """Итератор работает в цикле for."""
        p1 = Product("Т1", "О", 100.0, 1)
        p2 = Product("Т2", "О", 200.0, 2)
        cat = Category("Кат", "Описание", [p1, p2])
        names = []
        for product in CategoryIterator(cat):
            names.append(product.name)
        assert names == ["Т1", "Т2"]

    def test_iterator_returns_product_instances(self) -> None:
        """Итератор возвращает экземпляры Product."""
        p = Product("Товар", "О", 100.0, 1)
        cat = Category("Кат", "Описание", [p])
        for product in CategoryIterator(cat):
            assert isinstance(product, Product)

    def test_iterator_raises_stop_iteration(self) -> None:
        """Итератор выбрасывает StopIteration после последнего элемента."""
        p = Product("Товар", "О", 100.0, 1)
        cat = Category("Кат", "Описание", [p])
        it = CategoryIterator(cat)
        next(it)
        with pytest.raises(StopIteration):
            next(it)

    def test_iter_returns_self(self) -> None:
        """__iter__ возвращает сам итератор."""
        cat = Category("Кат", "Описание", [])
        it = CategoryIterator(cat)
        assert iter(it) is it


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
