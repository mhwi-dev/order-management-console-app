
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from repositories.order_repo import OrderRepo
from repositories.user_repo import UserRepo
from repositories.cart_repo import CartRepo
from repositories.product_repo import ProductRepo

from services.order_service import OrderService
from services.user_service import UserService
from services.cart_service import CartService
from services.product_service import ProductService

from models.cart import CartItem
from models.product import Product


def make_service(tmp_path):
    order_repo = OrderRepo(file_path=str(tmp_path / "orders.json"))
    user_repo = UserRepo(file_path=str(tmp_path / "users.json"))
    cart_repo = CartRepo(file_path=str(tmp_path / "carts.json"))
    product_repo = ProductRepo(file_path=str(tmp_path / "products.json"))

    user_service = UserService(user_repo)
    product_service = ProductService(product_repo)
    cart_service = CartService(cart_repo)

    order_service = OrderService(
        order_repo,
        user_service,
        cart_service,
        product_service
    )

    return order_service, user_service, cart_service, product_service


def make_user(user_service):
    return user_service.sign_up(
        username="testuser",
        password="123456",
        full_name="Test User",
        role="customer"
    )


def make_product(product_service):
    return product_service.add_new_product("Coffee", 35000, 10)


def make_cart_item(product, quantity=2, note=""):
    return CartItem(
        product=product,
        quantity=quantity,
        note=note
    )


def test_place_order_success(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    user = make_user(user_service)
    product = make_product(product_service)

    cart_item = make_cart_item(product, quantity=2, note="Less sweet")

    order = service.place_order(
        user_id=user.user_id,
        order_type="To go",
        address="297/9",
        select_items=[cart_item]
    )

    assert order.order_id == 1
    assert order.user_id == user.user_id
    assert order.total == 70000
    assert order.status == "pending"

    assert order.items[product.product_id].quantity == 2
    assert order.items[product.product_id].note == "Less sweet"

    updated_product = product_service.get_product_by_id(product.product_id)
    assert updated_product.stock == 8

    assert service.order_repo.get_next_id() == 2


def test_place_order_empty_items(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    with pytest.raises(ValueError):
        service.place_order(
            user_id=1,
            order_type="To go",
            address="297/9",
            select_items=[]
        )

    assert service.order_repo.get_next_id() == 1


def test_place_order_user_not_exists(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    product = make_product(product_service)
    cart_item = make_cart_item(product)

    with pytest.raises(ValueError):
        service.place_order(
            user_id=999,
            order_type="To go",
            address="297/9",
            select_items=[cart_item]
        )

    assert product_service.get_product_by_id(product.product_id).stock == 10
    assert service.order_repo.get_next_id() == 1


def test_place_order_product_not_exists(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    user = make_user(user_service)

    product = Product(
        product_id=999,
        name="Ghost Coffee",
        price=35000,
        stock=10
    )

    cart_item = make_cart_item(product)

    with pytest.raises(ValueError):
        service.place_order(
            user_id=user.user_id,
            order_type="To go",
            address="297/9",
            select_items=[cart_item]
        )

    assert service.order_repo.get_next_id() == 1


def test_place_order_insufficient_stock(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    user = make_user(user_service)
    product = make_product(product_service)

    cart_item = make_cart_item(product, quantity=11)

    with pytest.raises(ValueError):
        service.place_order(
            user_id=user.user_id,
            order_type="To go",
            address="297/9",
            select_items=[cart_item]
        )

    updated_product = product_service.get_product_by_id(product.product_id)

    assert updated_product.stock == 10
    assert service.order_repo.get_next_id() == 1


def test_place_order_uses_current_product_price(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    user = make_user(user_service)
    product = make_product(product_service)

    old_product = Product(
        product_id=product.product_id,
        name=product.name,
        price=30000,
        stock=product.stock
    )

    cart_item = make_cart_item(old_product, quantity=2)

    product_service.update_product(product.product_id, price=40000)

    order = service.place_order(
        user_id=user.user_id,
        order_type="To go",
        address="297/9",
        select_items=[cart_item]
    )

    assert order.total == 80000
    assert order.items[product.product_id].product.price == 40000


def test_place_order_validate_all_products_before_reducing_stock(tmp_path):
    service, user_service, cart_service, product_service = make_service(tmp_path)

    user = make_user(user_service)

    product_1 = product_service.add_new_product("Coffee", 35000, 10)
    product_2 = product_service.add_new_product("Cake", 40000, 1)

    items = [
        make_cart_item(product_1, quantity=2),
        make_cart_item(product_2, quantity=3)
    ]

    with pytest.raises(ValueError):
        service.place_order(
            user_id=user.user_id,
            order_type="To go",
            address="297/9",
            select_items=items
        )

    updated_product_1 = product_service.get_product_by_id(product_1.product_id)
    updated_product_2 = product_service.get_product_by_id(product_2.product_id)

    assert updated_product_1.stock == 10
    assert updated_product_2.stock == 1

    assert service.order_repo.get_next_id() == 1
