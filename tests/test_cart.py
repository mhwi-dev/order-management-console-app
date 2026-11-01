import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.product import Product
from services.cart_service import CartService
from repositories.cart_repo import CartRepo

def make_service(tmp_path):
    repo = CartRepo(file_path=str(tmp_path/'carts.json'))
    return CartService(repo)

def test_add_to_cart_success(tmp_path):
    service = make_service(tmp_path)
    product = Product(1, "Peach Tea", 55000, 15)

    user_cart = service.add_to_cart(101, product, 10, 'less sweet')

    assert user_cart.user_id == 101
    assert user_cart.items[1].quantity == 10
    assert user_cart.items[1].note == 'less sweet'

def test_add_multiple_products_to_cart(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    user_cart = service.add_to_cart(101, product_1, 10, 'less sweet')
    user_cart = service.add_to_cart(101, product_2, 1, 'no sugar')

    assert user_cart.user_id == 101

    assert user_cart.items[1].quantity == 10
    assert user_cart.items[2].quantity == 1

    assert user_cart.items[1].note == 'less sweet'
    assert user_cart.items[2].note == 'no sugar'

    assert user_cart.items[1].product.name == "Peach Tea"
    assert user_cart.items[2].product.name == "Ice Latte"

    assert len(user_cart.items) == 2

def test_add_same_product_increases_quantity(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)

    user_cart = service.add_to_cart(101, product_1, 2, 'less sweet')
    user_cart = service.add_to_cart(101, product_1, 3, 'less sweet')

    assert user_cart.items[1].quantity == 5

    assert len(user_cart.items) == 1

def test_add_same_product_updates_note(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)

    user_cart = service.add_to_cart(101, product_1, 2, 'less sweet')
    user_cart = service.add_to_cart(101, product_1, 3, 'no sugar')

    assert user_cart.items[1].quantity == 5

    assert user_cart.items[1].note == 'no sugar'

def test_add_same_product_keeps_old_note_when_new_note_empty(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)

    user_cart = service.add_to_cart(101, product_1, 2, 'less sweet')
    user_cart = service.add_to_cart(101, product_1, 3, '')

    assert user_cart.items[1].quantity == 5

    assert user_cart.items[1].note == 'less sweet'

def test_get_cart_by_id_success(tmp_path):
    service = make_service(tmp_path)

    product = Product(1, "Peach Tea", 55000, 15)
    
    service.add_to_cart(101, product, 2, 'less sweet')

    user_cart = service.get_cart_by_id(101)

    assert user_cart is not None
    assert user_cart.user_id == 101
    assert user_cart.items[1].product.name == 'Peach Tea'
    assert user_cart.items[1].quantity == 2

def test_get_cart_by_id_not_found(tmp_path):
    service = make_service(tmp_path)
    user_cart = service.get_cart_by_id(999)

    assert user_cart is None

def test_show_empty_cart(tmp_path):
    service = make_service(tmp_path)
    user_cart = service.show_cart_details(999)

    assert user_cart == (0, [])

def test_show_cart_details_success(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    service.add_to_cart(101, product_1, 1, 'less sweet')
    service.add_to_cart(101, product_2, 1, 'no sugar')

    user_cart= service.show_cart_details(101)

    assert user_cart[0] == 105000
    assert len(user_cart[1]) == 2

    assert user_cart[1][0]["name"] == "Peach Tea"
    assert user_cart[1][0]["total"] == 55000

    assert user_cart[1][1]["name"] == "Ice Latte"
    assert user_cart[1][1]["total"] == 50000

def test_remove_one_item_from_cart_success(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    service.add_to_cart(101, product_1, 1, 'less sweet')
    service.add_to_cart(101, product_2, 1, 'no sugar')

    service.remove_items_from_cart(101, [1])

    user_cart = service.get_cart_by_id(101)

    assert user_cart.items[2].product.name == 'Ice Latte'

    assert len(user_cart.items) == 1
    assert 1 not in user_cart.items

def test_remove_items_from_nonexistent_cart(tmp_path):
    service = make_service(tmp_path)

    user_cart = service.remove_items_from_cart(999, [1])

    assert user_cart == 0

def test_remove_multiple_items_from_cart(tmp_path):
    service = make_service(tmp_path)

    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)
    product_3 = Product(3, "Americano", 40000, 10)

    service.add_to_cart(101, product_1, 1, 'less sweet')
    service.add_to_cart(101, product_2, 1, 'no sugar')
    service.add_to_cart(101, product_3, 1, '')

    service.remove_items_from_cart(101, [1,2])

    user_cart = service.get_cart_by_id(101)

    assert len(user_cart.items) == 1
    assert 3 in user_cart.items
    assert 1 not in user_cart.items
    assert 2 not in user_cart.items

def test_remove_all_items_from_cart(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    service.add_to_cart(101, product_1, 1, 'less sweet')
    service.add_to_cart(101, product_2, 1, 'no sugar')

    service.remove_items_from_cart(101, [1,2])

    user_cart = service.get_cart_by_id(101)
    
    assert user_cart.items == {}

def test_add_to_cart_creates_new_cart(tmp_path):
    service = make_service(tmp_path)
    product = Product(1, "Peach Tea", 55000, 15)

    user_cart = service.add_to_cart(101, product, 10, 'less sweet')

    assert user_cart.user_id == 101
    assert len(user_cart.items) == 1
    assert user_cart.items[1].quantity == 10

def test_add_to_cart_different_users(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    user_cart_1 = service.add_to_cart(101, product_1, 1, 'less sweet')
    user_cart_2 = service.add_to_cart(102, product_2, 1, 'no sugar')

    assert user_cart_1.user_id == 101
    assert user_cart_2.user_id == 102

    assert len(user_cart_1.items) == 1
    assert len(user_cart_2.items) == 1

    assert 1 in user_cart_1.items
    assert 2 not in user_cart_1.items

    assert 2 in user_cart_2.items
    assert 1 not in user_cart_2.items

def test_get_cart_by_id_different_users(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    service.add_to_cart(101, product_2, 3, '')
    service.add_to_cart(102, product_1, 2, 'No Peach')

    user_1 = service.get_cart_by_id(101)
    user_2 = service.get_cart_by_id(102)

    assert user_1.user_id == 101
    assert user_2.user_id == 102

    assert user_1.items[2].product.name == "Ice Latte"
    assert user_1.items[2].quantity == 3

    assert user_2.items[1].product.name == "Peach Tea"
    assert user_2.items[1].quantity == 2

def test_show_cart_details_calculates_total_correctly(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    service.add_to_cart(101, product_1, 2, '')
    service.add_to_cart(101, product_2, 3, 'No Peach')

    user_cart = service.show_cart_details(101)

    assert user_cart[0] == 260000
    assert len(user_cart[1]) == 2

    assert user_cart[1][0]['quantity'] == 2
    assert user_cart[1][1]['quantity'] == 3

    assert user_cart[1][0]['total'] == 110000
    assert user_cart[1][1]['total'] == 150000

def test_add_to_cart_zero_quantity(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)

    with pytest.raises(ValueError):
        service.add_to_cart(101, product_1, 0, '')

def test_add_to_cart_negative_quantity(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)

    with pytest.raises(ValueError):
        service.add_to_cart(101, product_1, -1, '')

def test_add_to_cart_exceeds_stock(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)

    with pytest.raises(ValueError):
        service.add_to_cart(101, product_1, 16, '')

def test_add_to_cart_exceeds_stock_after_accumulating(tmp_path):
    service = make_service(tmp_path)
    product = Product(1, "Peach Tea", 55000, 15)

    service.add_to_cart(101, product, 10, '')

    with pytest.raises(ValueError):
        service.add_to_cart(101, product, 6, '')

def test_remove_multiple_items_returns_removed_count(tmp_path):
    service = make_service(tmp_path)
    product_1 = Product(1, "Peach Tea", 55000, 15)
    product_2 = Product(2, "Ice Latte", 50000, 17)

    service.add_to_cart(101, product_1, 2, '')
    service.add_to_cart(101, product_2, 3, 'No Sugar')

    user_cart = service.remove_items_from_cart(101, [1,2])

    assert user_cart == 2

def test_remove_items_with_existing_and_nonexistent_ids(tmp_path):
    service = make_service(tmp_path)

    product = Product(1, "Peach Tea", 55000, 15)
    service.add_to_cart(101, product, 2, '')

    removed_count = service.remove_items_from_cart(101, [1, 99])

    assert removed_count == 1

    user_cart = service.get_cart_by_id(101)
    assert user_cart.items == {}

from unittest.mock import patch

def test_remove_nonexistent_product_does_not_save(tmp_path):
    service = make_service(tmp_path)

    product = Product(1, "Peach Tea", 55000, 15)
    service.add_to_cart(101, product, 2, '')

    with patch.object(service.cart_repo, "save") as mock_save:
        removed_count = service.remove_items_from_cart(101, [99])

        assert removed_count == 0
        mock_save.assert_not_called()