import pytest
from _pytest.python_api import raises

from homework.models import Product, Cart

"""
Протестируйте классы из модуля homework/models.py
"""


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def apple():
    return Product("apple", 100, "This is a apple", 500)


@pytest.fixture
def cart(product):
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(999)
        assert product.check_quantity(1000)

    def test_product_check_quantity_more_than_available(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1001) == False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(1000)
        assert product.check_quantity(1) == False

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with raises(ValueError):
            product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product_first(self, cart, product):
        cart.add_product(product, 300)
        assert cart.products[product] == 300

    def test_add_product_of_the_earlier_added(self, cart, product):
        cart.add_product(product, 300)
        cart.add_product(product, 200)
        assert cart.products[product] == 500

    def test_add_product_more_than_there_is(self, cart, product):
        with raises(ValueError):
            cart.add_product(product, 1001)

    def test_del_when_quantity_not_transmitted(self, cart, product, apple):
        cart.add_product(product, 300)
        cart.add_product(apple, 400)
        cart.remove_product(product)
        assert cart.products.get(product) == None and cart.products.get(apple) == 400

    def test_del_when_quantity_is_less_than_in_cart(self, cart, product, apple):
        cart.add_product(product, 300)
        cart.add_product(apple, 400)
        cart.remove_product(product, 100)
        cart.remove_product(apple, 300)
        assert cart.products.get(product) == 200 and cart.products.get(apple) == 100

    def test_del_when_quantity_is_more_than_in_cart(self, cart, product, apple):
        cart.add_product(product, 300)
        cart.add_product(apple, 500)
        cart.remove_product(product, 301)
        assert cart.products.get(product) == None and cart.products.get(apple) == 500

    def test_del_all_products_in_cart(self, cart, product, apple):
        cart.add_product(product, 300)
        cart.add_product(apple, 500)
        assert len(cart.products) == 2
        cart.products.clear()
        assert len(cart.products) == 0

    def test_total_price(self, cart, product, apple):
        cart.add_product(product, 3)
        cart.add_product(apple, 5)
        assert cart.get_total_price() == 800.0

    def test_buy_products(self, cart, product, apple):
        cart.add_product(product, 200)
        cart.add_product(apple, 100)
        cart.buy()
        assert product.quantity == 800 and apple.quantity == 400
        assert len(cart.products) == 0

    def test_buy_products_when_quantity_is_less_than_in_cart(self, cart, product):
        cart.add_product(product, 200)
        product.quantity = 100
        with raises(ValueError):
            cart.buy()
