"""Тесты утилиты загрузки данных из JSON."""

import json
from typing import Any

import pytest

from src.classes import Category, Product
from src.utils import load_from_json


@pytest.fixture(autouse=True)
def reset_counters() -> None:  # type: ignore[misc]
    """Сбрасывает счётчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture()
def sample_json(tmp_path: Any) -> str:
    """Создаёт временный JSON-файл с тестовыми данными."""
    data = [
        {
            "name": "Электроника",
            "description": "Все виды электроники",
            "products": [
                {
                    "name": "Телефон",
                    "description": "Смартфон",
                    "price": 50000.0,
                    "quantity": 10,
                },
                {
                    "name": "Планшет",
                    "description": "Большой экран",
                    "price": 30000.0,
                    "quantity": 5,
                },
            ],
        },
        {
            "name": "Одежда",
            "description": "Модная одежда",
            "products": [
                {
                    "name": "Футболка",
                    "description": "Хлопок",
                    "price": 1500.0,
                    "quantity": 100,
                }
            ],
        },
    ]
    path = str(tmp_path / "products.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return path


@pytest.fixture()
def empty_json(tmp_path: Any) -> str:
    """Создаёт временный JSON-файл с пустым списком категорий."""
    path = str(tmp_path / "empty.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump([], f)
    return path


@pytest.fixture()
def no_products_json(tmp_path: Any) -> str:
    """Создаёт JSON-файл с категорией без товаров."""
    data = [{"name": "Пустая", "description": "Без товаров", "products": []}]
    path = str(tmp_path / "no_products.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return path


class TestLoadFromJson:
    """Тесты функции load_from_json."""

    def test_returns_list(self, sample_json: str) -> None:
        """Функция возвращает список."""
        result = load_from_json(sample_json)
        assert isinstance(result, list)

    def test_categories_count(self, sample_json: str) -> None:
        """Количество загруженных категорий соответствует JSON."""
        result = load_from_json(sample_json)
        assert len(result) == 2

    def test_categories_are_category_instances(self, sample_json: str) -> None:
        """Элементы списка — экземпляры Category."""
        result = load_from_json(sample_json)
        for cat in result:
            assert isinstance(cat, Category)

    def test_category_name(self, sample_json: str) -> None:
        """Имя категории загружается корректно."""
        result = load_from_json(sample_json)
        assert result[0].name == "Электроника"
        assert result[1].name == "Одежда"

    def test_category_description(self, sample_json: str) -> None:
        """Описание категории загружается корректно."""
        result = load_from_json(sample_json)
        assert result[0].description == "Все виды электроники"

    def test_products_loaded(self, sample_json: str) -> None:
        """Товары внутри категории загружаются."""
        result = load_from_json(sample_json)
        assert len(result[0].products) == 2
        assert len(result[1].products) == 1

    def test_product_attributes(self, sample_json: str) -> None:
        """Атрибуты товара загружаются корректно."""
        result = load_from_json(sample_json)
        p = result[0].products[0]
        assert p.name == "Телефон"
        assert p.description == "Смартфон"
        assert p.price == 50000.0
        assert p.quantity == 10

    def test_products_are_product_instances(self, sample_json: str) -> None:
        """Товары — экземпляры класса Product."""
        result = load_from_json(sample_json)
        for cat in result:
            for p in cat.products:
                assert isinstance(p, Product)

    def test_class_counters_updated(self, sample_json: str) -> None:
        """Счётчики Category обновляются при загрузке."""
        load_from_json(sample_json)
        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_empty_json(self, empty_json: str) -> None:
        """Пустой JSON возвращает пустой список."""
        result = load_from_json(empty_json)
        assert result == []

    def test_category_without_products(self, no_products_json: str) -> None:
        """Категория без товаров загружается корректно."""
        result = load_from_json(no_products_json)
        assert len(result) == 1
        assert result[0].products == []
        assert Category.product_count == 0
